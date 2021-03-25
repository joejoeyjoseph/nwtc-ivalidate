# compare.py
#
# This script runs the comparison between timeseries data,
# as specified in config.yaml
#
# Joseph Lee <joseph.lee@pnnl.gov>

import yaml
import sys
import importlib
import os
import pathlib
import numpy as np
import pandas as pd

from tools import eval_tools, cal_print_metrics

# config_file = str(pathlib.Path(os.getcwd()).parent)+'/config.yaml'
config_file = str(pathlib.Path(os.getcwd()).parent)+'/config_test.yaml'

sys.path.append('.')

conf = yaml.load(open(config_file), Loader=yaml.FullLoader)

base = conf['base']
comp = conf['comp']
p_curve = conf['power_curve']

# Pre-load all the metric modules into an array
metrics = [eval_tools.get_module_class('metrics', m)()
           for m in conf['metrics']]

print('validation start time:', conf['time']['window']['lower'])
print('validation end time:', conf['time']['window']['upper'])
print('location:', conf['location'])
print('baseline dataset:', base['name'])
print('variable:', conf['plot']['var'])

crosscheck_ts = eval_tools.get_module_class('qc', 'crosscheck_ts')(conf)

plotting = eval_tools.get_module_class('plotting', 'plot_data')(conf)

all_lev_df = pd.DataFrame()

for lev in conf['levels']['height_agl']:

    print()
    print('######################### height a.g.l.: '+str(lev)
          + ' '+conf['levels']['height_units']+' #########################'
          )
    print()

    # Load the data and compute the metrics
    results = []

    print('********** for '+base['name']+': **********')

    # run __init__
    base['input'] = eval_tools.get_module_class('inputs', base['function'])(
        base['path'], base['var'], base['target_var']
        )

    base['data'] = base['input'].get_ts(lev, base['freq'], base['flag'])

    for ind, c in enumerate(comp):

        print()
        print('********** for '+c['name']+': **********')

        # run __init__
        c['input'] = eval_tools.get_module_class('inputs', c['function'])(
            c['path'], c['var'], c['target_var']
            )

        c['data'] = c['input'].get_ts(conf['location'], lev, c['freq'],
                                      c['flag']
                                      )

        results = eval_tools.append_results(results, base, c, conf)

        combine_df = crosscheck_ts.align_time(base['data'], c['data'])

        cal_print_metrics.run(
            combine_df, metrics, results, ind, c, conf, base, lev
            )

        plotting.plot_ts_line(combine_df, lev)
        plotting.plot_histogram(combine_df, lev)
        plotting.plot_pair_scatter(combine_df, lev)

        combine_df.columns = pd.MultiIndex.from_product([[lev],
                                                        combine_df.columns]
                                                        )

        if all_lev_df.empty:
            all_lev_df = all_lev_df.append(combine_df)
        else:
            all_lev_df = pd.concat([all_lev_df, combine_df], axis=1)

for ind, c in enumerate(comp):

    results = []

    # if both variables are wind speed
    # and hub height exists in validation levels
    if (
        base['nature'] == 'ws' and c['nature'] == 'ws'
        and p_curve['hub_height'] in all_lev_df.columns.get_level_values(0)
    ):

        print()
        print('######################### deriving wind power at '
              + str(p_curve['hub_height'])+' '+conf['levels']['height_units']
              + ' #########################')
        print()
        print('use power curve: '+p_curve['file'])

        hhws_df = all_lev_df.xs(p_curve['hub_height'], level=0, axis=1)

        pc_csv = eval_tools.get_module_class('inputs', p_curve['function'])(
            p_curve['path'], p_curve['file'], p_curve['ws'],
            p_curve['power'], hhws_df, p_curve['hub_height'], conf
            )

        power_df = pc_csv.get_power()

        results = eval_tools.append_results(results, base, c, conf)

        cal_print_metrics.run(
            power_df, metrics, results, ind, c, conf, base,
            p_curve['hub_height']
            )
        
        # plot simulated power curves, not extremely useful
        # p_curve['input'].plot_pc()
        pc_csv.plot_power_ts()

        pc_csv.plot_power_scatter()

    else:

        print('either baseline and compare data are not wind speed, '
              + 'or hub height does not exist in validation data, '
              + 'hence power curve is not derived'
              )
