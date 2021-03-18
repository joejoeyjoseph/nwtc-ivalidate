# mae.py
#
# This is a simple average mae calculation, mae = mean(|x - y|). 
#
# If the input vectors differ, it takes the first N elements of each
# so that the size is the same. Error is computed pairwise without regard
# to the timestamps.
#
# Joseph Lee <joseph.lee@nrel.gov>

import numpy as np

class mae:

  def compute(self,x,y):

    return float(np.mean(abs(x - y)))
