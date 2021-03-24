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
import itertools

config_file = str(pathlib.Path(os.getcwd()).parent)+'/config.yaml'
# config_file = str(pathlib.Path(os.getcwd()).parent)+'/config_test.yaml'

sys.path.append('.')

conf = yaml.load(open(config_file), Loader=yaml.FullLoader)

base = conf['base']
comp = conf['comp']
p_curve = conf['power_curve']

print(p_curve)


# Load the module t class with the name s
def get_module_class(t, s):

    m = importlib.import_module('.'.join([t, s]))

    return getattr(m, s)


# Apply a series of transformative modules
def apply_trans(ts, modlist):

    for m in modlist:

        ts = m.apply(ts)

    return ts


# Pre-load all the metric modules into an array
metrics = [get_module_class('metrics', m)() for m in conf['metrics']]

print('validation start time:', conf['time']['window']['lower'])
print('validation end time:', conf['time']['window']['upper'])
print('location:', conf['location'])
print('baseline dataset:', base['name'])
print('variable:', conf['plot']['var'])

crosscheck_ts = get_module_class('qc', 'crosscheck_ts')(conf)

plotting = get_module_class('plotting', 'plot_data')(conf)

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
    base['input'] = get_module_class('inputs',
                                     base['function'])(base['path'],
                                                       base['var'],
                                                       base['target_var']
                                                       )

    base['data'] = base['input'].get_ts(lev, base['freq'], base['flag'])

    for ind, c in enumerate(comp):

        print()
        print('********** for '+c['name']+': **********')

        # run __init__
        c['input'] = get_module_class('inputs',
                                      c['function'])(c['path'], c['var'],
                                                     c['target_var']
                                                     )

        c['data'] = c['input'].get_ts(conf['location'], lev, c['freq'],
                                      c['flag']
                                      )

        results.append({'truth name': base['name'],
                        'model name': c['name'],
                        'path': c['path'],
                        'location': conf['location'],
                        'var': c['var']}
                       )

        combine_df = crosscheck_ts.align_time(base['data'], c['data'])

        compute_df = combine_df.dropna()

        only_na = combine_df[~combine_df.index.isin(compute_df.index)]

        print()
        print('to calculate metrics, removing the following time steps'
              + ' that contain NaN values:'
              )
        print(only_na.index.strftime('%Y-%m-%d %H:%M:%S').values)

        # for future purposes,
        # in case of reading in mulitple compare data columns
        for pair in itertools.combinations(compute_df.columns, 2):

            # baseline should be the 1st (Python's 0th) column
            x = compute_df[pair[0]]
            y = compute_df[pair[1]]

        if len(x) != len(y):

            sys.exit('Lengths of baseline and compare datasets are'
                     + ' not equal!'
                     )

        for m in metrics:

            results[ind][m.__class__.__name__] = m.compute(x, y)

        print()
        print('==-- '+conf['plot']['var']+' metrics: '+c['name']+' - '
              + base['name']+' at '+str(lev)+' '
              + conf['levels']['height_units']+' --=='
              )
        print()

        for key, val in results[0].items():
            if key != 'path':
                if isinstance(val, float):

                    end_units = ''
                    suffix_pct = 'pct'

                    if str(key).endswith(suffix_pct):
                        end_units = '%'

                    print(str(key)+': '+str(np.round(val, 3))+end_units)

        plotting.plot_ts_line(combine_df, lev)
        plotting.plot_histogram(combine_df, lev)
        plotting.plot_pair_scatter(combine_df, lev)

        combine_df.columns = pd.MultiIndex.from_product([[lev],
                                                        combine_df.columns]
                                                        )

        # print(combine_df.head())

        # print(combine_df.index)
        # print(all_lev_df.index)

        # print(all_lev_df.shape)

        if all_lev_df.empty:
            # print('here')
            all_lev_df = all_lev_df.append(combine_df)
        else:
            # all_lev_df = all_lev_df.merge(combine_df)
            all_lev_df = pd.concat([all_lev_df, combine_df], axis=1)

        # print(all_lev_df.shape)
        # print(all_lev_df.head())
        # print(all_lev_df.tail())

for ind, c in enumerate(comp):

    # print(base['nature'])
    # print(c['nature'])

    # if both variables are wind speed
    # and hub height exists in validation levels
    if (
        base['nature'] == 'ws' and c['nature'] == 'ws'
        and p_curve['hub_height'] in all_lev_df.columns.get_level_values(0)
    ):

        # plot_pcurve = get_module_class('plotting', 'plot_pc')(conf)

        hhws_df = all_lev_df.xs(p_curve['hub_height'], level=0, axis=1)

        # print(hh_df.head())

        pc_csv = get_module_class('inputs', p_curve['function'])(
            p_curve['path'], p_curve['file'], p_curve['ws'],
            p_curve['power'], hhws_df, p_curve['hub_height'], conf
            )

        # print(p_curve['input'])

        p_df = pc_csv.get_power()
        print(p_df.head())

        # plot simulated power curves, not extremely useful
        # p_curve['input'].plot_pc()

        pc_csv.plot_power_ts()

        pc_csv.tplot_power_ts()

        # plot_pcurve.plot_sct(hhws_df, p_df)

    else:

        print('either baseline and compare data are not wind speed, '
              + 'or hub height does not exist in validation data, '
              + 'hence power curve is not derived'
              )
