# Joseph Lee <joseph.lee@pnnl.gov>

import os
import pathlib
import importlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# from plotting import plot_data
from tools import module_tools


class pc_csv:

    def __init__(self, path, file, ws, power, hhws_df, hub_height, conf):

        self.path = str(pathlib.Path(os.getcwd()).parent)+'/'+str(path)
        self.file = self.path+'/'+file
        self.ws = ws
        self.power = power
        self.hhws_df = hhws_df
        self.hh = hub_height
        self.conf = conf
        self.conf['plot']['var'] = self.power

    def load_obj(self, metric):

        test_dir = 'plotting'

        metric_module = importlib.import_module('.'.join([test_dir, metric]))

        metric_obj = getattr(metric_module, metric)(self.conf)

        return metric_obj

    def tplot_power_ts(self):

        # metric_obj = self.load_obj('plot_data')

        # print(metric_obj)

        # metric_obj.plot_ts_line(self.p_df, self.hh, self_units=False)

        plotting = module_tools.get_module_class('plotting', 'plot_data')(
            self.conf)

        plotting.plot_ts_line(self.p_df, self.hh, self_units=False)

    def get_power(self):

        self.pc_df = pd.read_csv(self.file)

        p_df = pd.DataFrame(0, columns=self.hhws_df.columns+'_derived_power',
                            index=self.hhws_df.index)

        for i, row in self.pc_df.iterrows():

            for hh_col, p_col in zip(self.hhws_df.columns, p_df.columns):

                p_df.loc[self.hhws_df[hh_col] > row[self.ws], p_col]\
                    = row[self.power]

        self.p_df = p_df

        return self.p_df

    def plot_pc(self):

        plt.plot(self.pc_df[self.ws], self.pc_df[self.power], c='k')

        for hh_col, p_col in zip(self.hhws_df.columns, self.p_df.columns):

            plt.scatter(self.hhws_df[hh_col], self.p_df[p_col])

        plt.show()

    def plot_power_ts(self):

        for col in self.p_df.columns:

            plt.plot(self.p_df.index, self.p_df[col], label=col)

        plt.xticks(rotation=90)
        plt.legend()

        plt.xlabel('time')
        plt.ylabel(self.power)
        plt.title(self.power+' at '+str(self.hh)+' m a.g.l.')

        plt.show()

    def plot_pair_scatter(self):

        for pair in itertools.combinations(self.p_df.columns, 2):

            plt.scatter(self.p_df[pair[0]], self.p_df[pair[1]], c='k')

            cal_df = df.dropna()
            corr = np.corrcoef(cal_df[pair[0]], cal_df[pair[1]])[0, 1]

            line_min = np.nanmin([df[pair[0]], df[pair[1]]])
            line_max = np.nanmax([df[pair[0]], df[pair[1]]])
            xy1to1 = np.linspace(line_min*0.9, line_max*1.1)
            plt.plot(xy1to1, xy1to1, c='grey', linestyle='--')

            plt.xlabel(pair[0]+' ('+self.units+')')
            plt.ylabel(pair[1]+' ('+self.units+')')
            plt.title(self.var+' at '+str(lev)+' '+self.lev_units
                      + ' a.g.l., r = '+str(round(corr, 3))
                      )

            plt.show()
