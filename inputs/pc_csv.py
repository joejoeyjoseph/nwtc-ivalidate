# Joseph Lee <joseph.lee@pnnl.gov>

import os
import pathlib
import importlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tools import eval_tools


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

    def get_power(self):

        self.pc_df = pd.read_csv(self.file)

        power_df = pd.DataFrame(
            0, columns=self.hhws_df.columns+'_derived_power',
            index=self.hhws_df.index
            )

        for hh_col, p_col in zip(self.hhws_df.columns, power_df.columns):

            # when ws is nan, assign power to nan
            power_df.loc[np.isnan(self.hhws_df[hh_col]), p_col]\
                    = np.NaN

            for i, row in self.pc_df.iterrows():

                power_df.loc[self.hhws_df[hh_col] > row[self.ws], p_col]\
                    = row[self.power]

        self.power_df = power_df

        return self.power_df

    def plot_pc(self):

        plt.plot(self.pc_df[self.ws], self.pc_df[self.power], c='k')

        for hh_col, p_col in zip(self.hhws_df.columns, self.power_df.columns):

            plt.scatter(self.hhws_df[hh_col], self.power_df[p_col])

        plt.show()

    def plot_power_ts(self):

        plotting = eval_tools.get_module_class('plotting', 'plot_data')(
            self.conf)

        plotting.plot_ts_line(self.power_df, self.hh, self_units=False)
