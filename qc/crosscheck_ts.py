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

    return combine_df

  

  # def trim_ts: 

  # def time_align2(conf,x,y):

  #   print('iggg')

  #   # apply time window
  #   if "window" in list(conf.keys()):

  #       if conf["window"]["lower"].__class__.__name__ != 'datetime':
  #       lower = dateutil.parser.parse(conf["window"]["lower"])
  #       else:
  #       lower = conf["window"]["lower"]
  #       if conf["window"]["upper"].__class__.__name__ != 'datetime':
  #       upper = dateutil.parser.parse(conf["window"]["upper"])
  #       else:
  #       upper = conf["window"]["upper"]

  #       x = x[x.index <= upper]
  #       x = x[x.index >= lower]
  #       y = y[y.index <= upper]
  #       y = y[y.index >= lower]

  #   # trim to extent of base or comp
  #   if "trim" in list(conf.keys()):

  #       if conf["trim"] == "base":
  #       lower = x.index.min()
  #       upper = x.index.max()
  #       y = y[y.index <= upper]
  #       y = y[y.index >= lower]
  #       elif conf["trim"] == "comp":
  #       lower = y.index.min()
  #       upper = y.index.max()
  #       x = x[x.index <= upper]
  #       x = x[x.index >= lower]
        
  #   return (x,y)