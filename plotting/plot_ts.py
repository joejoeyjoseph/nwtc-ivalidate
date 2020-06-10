# plot_ts.py
# 
# Plot time series
# 
# Joseph Lee <joseph.lee@nrel.gov>

import pandas as pd
import matplotlib.pyplot as plt

class plot_ts:

  def plot_line(self):

    self['data'].plot()

    plt.ylabel(self['var'])
    plt.title(self['name'])

    plt.show()

  def plot_subset_line(self, data_name):

    self.plot()

    plt.ylabel(self.columns[0])
    plt.title(data_name)

    plt.show()

