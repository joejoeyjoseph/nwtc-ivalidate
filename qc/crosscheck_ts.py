# perform crosscheck of data

import pandas as pd
import numpy as np

class crosscheck_ts: 
  
  def __init__(self, conf):

    self.upper = conf['time']["window"]["upper"]
    self.lower = conf['time']["window"]["lower"]

  def trim_ts(self, ts):

    ts = ts.loc[ts.index >= self.lower]
    ts = ts.loc[ts.index <= self.upper]

    return ts

  def align_time(self, base, comp): 

    base = self.trim_ts(base)
    comp = self.trim_ts(comp)

    # match time series data frequencies
    # base ts as 1st column
    combine_df = pd.merge(base, comp, left_index=True, right_index=True)

    t_min = combine_df.index.min()
    t_max = combine_df.index.max()

    freq = (combine_df.index[1] - t_min).total_seconds() / 60.0
    diff_minute = (t_max - t_min).total_seconds() / 60.0

    print('evaluate from '+str(t_min)+' to '+str(t_max)+\
      ' every '+str(freq)+' minutes, total of '+str(len(combine_df))+' time steps')

    if len(combine_df) == (diff_minute + freq) / freq: 
      pass
    else: 
      print('COMBINE_DF FREQUENCY IS WRONG')

    return combine_df
