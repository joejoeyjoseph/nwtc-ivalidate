# plot_ts.py
# 
# Plot time series
# 
# Joseph Lee <joseph.lee@nrel.gov>

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class plot_ts:

    def __init__(self, conf): 

        self.var = conf['plot']['var']
        
        if conf['plot']['units'] == 'ms-1':
            
            self.units = r'm $s^{-1}$'

    def plot_line(self):

        self['data'].plot()

        plt.ylabel(self['var'])
        plt.title(self['name'])

        plt.show()

    def plot_subset_line(self, data_name, lev):

        self.plot()

        plt.ylabel(self.columns[0]+' at '+str(lev)+' m a.g.l.')
        plt.title(data_name)

        plt.show()

    def plot_pair_lines(self, df, lev): 

        print(df.iloc[15:30])

        ax = sns.lineplot(data=df)

        ax.set_xlabel('time')
        ax.set_ylabel(self.var)

        print(df.index.min())
        print(type(df.index.min()))
        print(df.index.max())

        import datetime
        date_time_obj = datetime.datetime.strptime('2016-09-23 18:00:00', '%Y-%m-%d %H:%M:%S')
        print(date_time_obj)

        ax.set_xlim(df.index.min(), date_time_obj)

        plt.xticks(rotation=90) 

        plt.show()

    def plot_pair_lines2(self, df, lev): 

        for col in df.columns: 
            
            plt.plot(df.index, df[col], label=col)

        # plt.plot(df.index, df['sodar_ws'])
        # plt.plot(df.index, df['wrf_ws'])

        plt.xticks(rotation=90) 
        plt.legend()

        plt.xlabel('time')
        plt.ylabel(self.var+' ('+self.units+')')
        plt.title(self.var+' at '+str(lev)+' m a.g.l.')

        plt.show()
