# calculate and print metrics results

import numpy as np
import itertools


def run(combine_df, metrics, results, ind, c, conf, base, lev):

    compute_df = combine_df.dropna()

    only_na = combine_df[~combine_df.index.isin(compute_df.index)]

    print()
    print('to calculate metrics, removing the following time steps'
          + ' that contain NaN values:'
          )
    print(only_na.index.strftime('%Y-%m-%d %H:%M:%S').values)
    print()
    print('hence, only use '+str(len(compute_df))
          + ' time steps in data to calculate metrics')

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
