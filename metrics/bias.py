# bias.py
#
# This is a simple average bias calculation, bias = mean(x - y), 
# assuming x is the truth. 
#
# If the input vectors differ, it takes the first N elements of each
# so that the size is the same. Error is computed pairwise without regard
# to the timestamps.
#
# Joseph Lee <joseph.lee@nrel.gov>


import numpy as np

class bias:

  def compute(self,x,y):
    
    # just values (second member of tuple)
    # note: this isn't time aligning at all, just compares the 
    #       values as they arrive
    x = x.to_numpy()[:,0]
    y = y.to_numpy()[:,0]

    # naively truncate longer array if one is shorter
    if len(x) > len(y):
      x = x[0:len(y)]
    if len(y) > len(x):
      y = y[0:len(x)]

    return float(np.mean(np.array(x) - np.array(y)))
