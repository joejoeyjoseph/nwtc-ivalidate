# linear_interp.py
#
# Perform a linear interpolation for the given period or sample size.
#
# Caleb Phillips <caleb.phillips@nrel.gov>
# Joseph Lee <joseph.lee@nrel.gov>

import numpy as np
import pandas as pd
import time
import datetime
import math

class linear_interp:

  def __init__(self,config):
    self.config = config

  def get_sample_ts(self,t):

    tmin = min(t)
    tmax = max(t)

    if "period" in list(self.config.keys()):
      period = self.config["period"]
      n = ((tmax-tmin)/period) + 1
    else:
      n = self.config["n"]

    return np.linspace(tmin,tmax,math.ceil(n))

  def apply(self,ts):
    
    t = [time.mktime(x.timetuple()) for x in ts.index]
    v = ts.to_numpy()[:,0]

    tprime = self.get_sample_ts(t)
    vprime = np.interp(tprime,t,v)

    tprime = [datetime.datetime.fromtimestamp(x) for x in tprime]
    
    return pd.DataFrame(index=tprime,data={ts.columns[0]: vprime})
