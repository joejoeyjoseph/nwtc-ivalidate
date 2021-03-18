# compare.py
#
# This script runs the comparison between timeseries data, 
# as specified in config.yaml
#
# Joseph Lee <joseph.lee@pnnl.gov>

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

# config_file = str(pathlib.Path(os.getcwd()).parent) + '/config.yaml'
config_file = str(pathlib.Path(os.getcwd()).parent) + '/config_test.yaml'

sys.path.append('.')

#conf = yaml.load(open(sys.argv[1]), Loader=yaml.FullLoader)
conf = yaml.load(open(config_file), Loader=yaml.FullLoader)

base = conf['base']
comp = conf['comp']

# Load the module t class with the name s
def get_module_class(t,s):

    m = importlib.import_module(".".join([t,s]))

    return getattr(m,s)

# Apply a series of transformative modules
def apply_trans(ts,modlist):

  for m in modlist:

    ts = m.apply(ts)

  return ts

# Pre-load all the metric modules into an array
metrics = [get_module_class("metrics",m)() for m in conf["metrics"]]

print('validation start time:', conf['time']["window"]["lower"])
print('validation end time:', conf['time']["window"]["upper"])
print('location:', conf['location'])
print('baseline dataset:', base['name'])
print('variable:', conf['plot']['var'])

crosscheck_ts = get_module_class('qc', 'crosscheck_ts')(conf)

plotting = get_module_class('plotting', 'plot_data')(conf)

for lev in conf['levels']['height_agl']: 

    print()
    print('######################### height a.g.l.: '+str(lev)+\
        ' '+conf['levels']['height_units']+' #########################'
        )
    print()

    # Load the data and compute the metrics
    results = []

    print('********** for '+base['name']+': **********')

    # run __init__
    base["input"] = get_module_class("inputs",base["format"])(base["path"], \
        base["var"], base['target_var']
        )

    base["data"] = base["input"].get_ts(lev, base['freq'], base['flag'])

    for ind, c in enumerate(comp):

        print()
        print('********** for '+c['name']+': **********')

        # run __init__
        c["input"] = get_module_class("inputs", c["format"])(c["path"], \
            c["var"],c['target_var']
            )

        c["data"] = c["input"].get_var_ts(conf["location"], lev, c['freq'], \
            c['flag']
            )

        results.append({'truth name': base['name'], 'model name': c['name'], \
                        "path": c["path"], \
                        "location": conf["location"], "var": c["var"]}
                        )

        combine_df = crosscheck_ts.align_time(base["data"], c["data"])

        compute_df = combine_df.dropna()

        only_na = combine_df[~combine_df.index.isin(compute_df.index)]
        print()
        print('to calculate metrics, removing the following time steps'+\
            ' that contain NaN values:'
            )
        print(only_na.index.strftime("%Y-%m-%d %H:%M:%S").values)

        # for future purposes, 
        # in case of reading in mulitple compare data columns
        for pair in itertools.combinations(compute_df.columns, 2): 

            # baseline should be the 1st (Python's 0th) column
            x = compute_df[pair[0]]
            y = compute_df[pair[1]]

        if len(x) != len(y): 

            sys.exit('Lengths of baseline and compare datasets are'+\
                ' not equal!'
                )

        for m in metrics: 

            results[ind][m.__class__.__name__] = m.compute(x, y)

        print()
        print(conf['plot']['var']+' metrics: '+c['name']+' - '+base['name']+\
            ' at '+str(lev)+' '+conf['levels']['height_units']
            )
        print()
        for key, val in results[0].items():
            if key != 'path': 
                if isinstance(val, float): 
                    print(str(key)+': '+str(np.round(val, 3)))

        plotting.plot_pair_lines(combine_df, lev)
        plotting.plot_pair_scatter(combine_df, lev)
