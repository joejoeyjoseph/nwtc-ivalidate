# linear_interp.py
#
# Perform a linear interpolation for the given period or sample size.
#
# Caleb Phillips <caleb.phillips@nrel.gov>

import numpy as np
import pandas as pd
import time
import datetime
import math

class linear_interp:

  def __init__(self,config):
    self.config = config

  def get_sample_ts(self,t):
    #print(list(t)[0])
    #print(np.min(list(t)))
    #a = list(t)
    #print(type(a))
    #print(dir(a))
    #print(a)
    #t = list(t)
    tmin = min(t)
    tmax = max(t)
    print(list(self.config.keys()))
    if "period" in list(self.config.keys()):
      period = self.config["period"]
      print(period)
      n = ((tmax-tmin)/period) + 1
      print('get n1')
      print(n)
      print(math.ceil(n))
    else:
      n = self.config["n"]
      print('get n2')

    print(tmin,tmax,n)
    
    return np.linspace(tmin,tmax,math.ceil(n))

  def apply(self,ts):
    #t = map(lambda x: time.mktime(x.timetuple()),ts.index)
    t = [time.mktime(x.timetuple()) for x in ts.index]
    # t = list(map(lambda x: time.mktime(x.timetuple()),ts.index))
    # t = list([time.mktime(x.timetuple()) for x in ts.index])
    a = lambda x: time.mktime(x.timetuple()),ts.index
    print(a)

    # t = []
    # for i in ts.index: 
    #   t.append(time.mktime(i.timetuple())) 

    print('ttttt')
    print(t)
    #print(list(t))
    #t = list(t)
    #print(min(t))

    print(ts)

    #print(ts[:,0])
    #v = ts.as_matrix()[:,0]
    v = ts.to_numpy()[:,0]
    #print(v)
    tprime = self.get_sample_ts(t)
    vprime = np.interp(tprime,t,v)
    #tprime = map(lambda x: datetime.datetime.fromtimestamp(x),tprime)
    tprime = [datetime.datetime.fromtimestamp(x) for x in tprime]
    return pd.DataFrame(index=tprime,data={ts.columns[0]: vprime})
