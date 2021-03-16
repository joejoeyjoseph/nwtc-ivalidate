# plot_data.py
# 
# Plot data
# 
# Joseph Lee <joseph.lee@nrel.gov>

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import itertools

class plot_data:

    def __init__(self, conf): 

        self.var = conf['plot']['var']
        self.lev_units = conf['levels']['height_units']
        
        if conf['plot']['units'] == 'ms-1':
            
            self.units = r'm $s^{-1}$'

    def plot_pair_lines(self, df, lev): 

        for col in df.columns: 
            
            plt.plot(df.index, df[col], label=col)

        plt.xticks(rotation=90) 
        plt.legend()

        plt.xlabel('time')
        plt.ylabel(self.var+' ('+self.units+')')
        plt.title(self.var+' at '+str(lev)+' m a.g.l.')

        plt.show()

    def plot_pair_scatter(self, df, lev): 

        for pair in itertools.combinations(df.columns, 2): 

            plt.scatter(df[pair[0]], df[pair[1]], c='k')

            line_min = np.nanmin([df[pair[0]], df[pair[1]]])
            line_max = np.nanmax([df[pair[0]], df[pair[1]]])
            xy1to1 = np.linspace(line_min*0.9, line_max*1.1)
            plt.plot(xy1to1, xy1to1, c='grey', linestyle='--')

            plt.xlabel(pair[0]+' ('+self.units+')')
            plt.ylabel(pair[1]+' ('+self.units+')')
            plt.title(self.var+' at '+str(lev)+' '+self.lev_units+' a.g.l.')

            plt.show()
