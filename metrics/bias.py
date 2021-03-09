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

  def compute(self, x, y):

    return float(np.mean(x - y))
