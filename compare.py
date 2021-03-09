# compare.py
#
# This script runs the comparison between timeseries data as specified in config.yaml
#
# Caleb Phillips <caleb.phillips@nrel.gov>
# Joseph Lee <joseph.lee@nrel.gov>

import yaml
import sys
import importlib
import json
import dateutil
import re
import base64
import requests
import os
import pathlib
import numpy as np
import pandas as pd
import itertools

config_file = str(pathlib.Path(os.getcwd()).parent) + '/config.yaml'

sys.path.append('.')

# Check options and load config
# if len(sys.argv) < 2:
#   print("Usage: python compare.py <config.yaml>")
#   quit()

#conf = yaml.load(open(sys.argv[1]), Loader=yaml.FullLoader)
conf = yaml.load(open(config_file), Loader=yaml.FullLoader)

base = conf['base']
comp = conf['comp']

# FIXME: validate configuration file and give nice errors
#        if something (necessary) is missing

# Load the module t class with the name s
def get_module_class(t,s):

  m = importlib.import_module(".".join([t,s]))

  return getattr(m,s)

# Apply a series of transformative modules
def apply_trans(ts,modlist):

  # print('modlist')
  # print(modlist)

  for m in modlist:
    ts = m.apply(ts)
    #print(ts)

  return ts

def get_dap_file(path,config):

  api_url = "https://dteuqmpcac.execute-api.us-west-2.amazonaws.com/test/request-data"
  out_dir = config["cache_dir"] + "/dap/" + path  
  credentials = base64.b64encode("%s:%s" % (config["login"], config["pass"]))
  auth = {"Authorization": "Basic %s" % credentials}

  params = {
    "output": "json",
    "filter": {
        "Dataset": path
        #"file_type": ["txt"],
        #"date_time": {
        #    "between": ["20160505000000", "20160507000000"]
        #}
    }
  }

  print(params)

  req = requests.post(api_url, headers=auth, data=json.dumps(params), verify=False)
  print(req.text)

# Figure out where the file is (local or remote)
# and fetch if necessary
def get_file(path,remote):

  proto = None
  m = re.match(r"([a-z]+)://(.*)",path,re.IGNORECASE)
  
  if m:
    proto = m.group(1)
    path = m.group(2)
  else:
    proto = "local"

  if proto == "local":
    return path
  elif proto == "dap":
    return get_dap_file(path,remote["dap"])

# Pre-load all the metric modules into an array
metrics = [get_module_class("metrics",m)() for m in conf["metrics"]]

# Pre-load all the qa/qc modules into an array
preproc = []
for q in conf["prepare"]:
  k,c = q.popitem()
  preproc.append(get_module_class("prepare",k)(c))

print('validation start time:', conf['time']["window"]["lower"])
print('validation end time:', conf['time']["window"]["upper"])
print('location:', conf['location'])
print('variable:', base['var'])
print('truth:', base['name'])

crosscheck_ts = get_module_class('qc', 'crosscheck_ts')(conf)

plotting = get_module_class('plotting', 'plot_ts')

for lev in conf['levels']['height_agl']: 

  print('')
  print('#########################################################################')
  print('')

  print('height a.g.l.:', str(lev))

  # Load the data and compute the metrics
  results = []

  # base["path"] = get_file(base["path"],conf["remote"])
  base["path"] = get_file(base["path"], None) # local files
  base["input"] = get_module_class("inputs",base["format"])(base["path"],base["var"])
  # base["data"] = apply_trans(base["input"].get_ts(conf["location"], lev), preproc)
  base["data"] = base["input"].get_ts(conf["location"], lev)

  # print('base')
  #print(type(base))
  #print(base["data"]) 

  for i in range(0,len(comp)):

    #comp[i]["path"] = get_file(comp[i]["path"],conf["remote"])
    comp[i]["path"] = get_file(comp[i]["path"], None) # local files
    comp[i]["input"] = get_module_class("inputs",comp[i]["format"])(comp[i]["path"],comp[i]["var"])

    # comp[i]["data"] = apply_trans(comp[i]["input"].get_var_ts(conf["location"], lev),preproc)
    comp[i]["data"] = comp[i]["input"].get_var_ts(conf["location"], lev)

    # print('comp')
    #print(type(comp[i]))
    #print(comp[i]["data"]) 

    results.append({'truth name': base['name'], 'model name': comp[i]['name'], "path": comp[i]["path"], \
                    "location": conf["location"], "var": comp[i]["var"]})

    combine_df = crosscheck_ts.align_time(base["data"], comp[i]["data"])

    compute_df = combine_df.dropna()

    # for future purposes, in case of reading in mulitple compare data columns
    for pair in itertools.combinations(compute_df.columns, 2): 

      x = compute_df[pair[0]]
      y = compute_df[pair[1]]

    if len(x) != len(y): 
      sys.exit('Lengths of baseline and compare datasets are not equal!')

  # pd.set_option("display.max_rows", None, "display.max_columns", None)

  #   print(x)

    for m in metrics:

      # x, y = time_align(conf["time"],base["data"],comp[i]["data"])
      # x, y = check_data.time_align2(conf["time"],base["data"],comp[i]["data"])

      results[i][m.__class__.__name__] = m.compute(x, y)

  #   print('model:', comp[i]['name'])
  #   plotting.plot_subset_line(y, comp[i]['name'], lev)

  # print('truth:')
  # plotting.plot_subset_line(x, base['name'], lev)

  # # FIXME: allow different output formats besides JSON

  # # Output the results
  # #print(json.dumps(results))

  #print((results[0]['path']))
  for key, val in results[0].items():
    if key != 'path': 
      if isinstance(val, float): 
        print(str(key)+': '+str(np.round(val, 3)))
      # else: 
      #   print(str(key)+': '+str(val))
