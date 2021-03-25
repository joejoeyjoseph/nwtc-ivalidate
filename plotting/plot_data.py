# plot_data.py
#
# Plot data
#
# Joseph Lee <joseph.lee@pnnl.gov>

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
# from scipy import stats


class plot_data:

    def __init__(self, conf):

        self.var = conf['plot']['var']
        self.lev_units = conf['levels']['height_units']

        if conf['plot']['units'] == 'ms-1':

            self.units = r'm $s^{-1}$'

    def plot_ts_line(self, df, lev, self_units=True):

        for col in df.columns:

            plt.plot(df.index, df[col], label=col)

        plt.xticks(rotation=90)
        plt.legend()

        plt.xlabel('time')
        if self_units is True:
            plt.ylabel(self.var+' ('+self.units+')')
        else:
            plt.ylabel(self.var)
        plt.title(self.var+' at '+str(lev)+' m a.g.l.')

        plt.show()

    def plot_pair_scatter(self, df, lev):

        onetoone_c = 'grey'
        fit_c = 'green'

        for pair in itertools.combinations(df.columns, 2):

            fig, ax = plt.subplots()

            plt.scatter(df[pair[0]], df[pair[1]], c='k')

            cal_df = df.dropna()
            corr = np.corrcoef(cal_df[pair[0]], cal_df[pair[1]])[0, 1]

            line_min = np.nanmin([df[pair[0]], df[pair[1]]])
            line_max = np.nanmax([df[pair[0]], df[pair[1]]])
            xy1to1 = np.linspace(line_min*0.9, line_max*1.1)
            plt.plot(xy1to1, xy1to1, c=onetoone_c, linestyle='--')
            plt.text(0.95, 0.9, '1:1', c=onetoone_c, transform=ax.transAxes)

            plt.xlabel(pair[0]+' ('+self.units+')')
            plt.ylabel(pair[1]+' ('+self.units+')')
            # plt.title(self.var+' at '+str(lev)+' '+self.lev_units
            #           + ' a.g.l., r = '+str(round(corr, 3))
            #           )

            compute_df = df.dropna()
            x_fit = compute_df[pair[0]]
            y_fit = compute_df[pair[1]]

            coeffs = np.polyfit(x_fit, y_fit, 1)
            model_fn = np.poly1d(coeffs)

            yhat = model_fn(x_fit)
            ybar = np.sum(y_fit)/len(y_fit)
            ssreg = np.sum((yhat - ybar)**2)
            sstot = np.sum((y_fit - ybar)**2)
            r2 = ssreg/sstot

            # for linear regression, this works too
            # slope, intercept, r_value, p_value, std_err = stats.linregress(
            #     x_fit, y_fit)

            x_s = np.arange(compute_df.min().min(), compute_df.max().max())
            plt.plot(x_s, model_fn(x_s), color=fit_c)

            plt.title(self.var+' at '+str(lev)+' '+self.lev_units
                      + ' a.g.l. \n linear fit: '+pair[0]+' = '
                      + str(round(coeffs[0], 3))
                      + ' * '+pair[1]+' + '+str(round(coeffs[1], 3))
            )

            plt.show()

    def plot_histogram(self, df, lev):

        for col in df.columns:

            plt.hist(df[col], bins=15, alpha=0.4, label=col)

        plt.legend()

        plt.xlabel(self.var+' ('+self.units+')')
        plt.ylabel('count')
        plt.title(self.var+' at '+str(lev)+' m a.g.l.')

        plt.show()
