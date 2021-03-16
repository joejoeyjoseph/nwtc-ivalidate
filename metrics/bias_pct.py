# bias_pct.py
#
# This is a simple average percent bias calculation, bias % = mean(100 * (x - y) / x), 
# assuming x is the truth. 
#
# If the input vectors differ, it takes the first N elements of each
# so that the size is the same. Error is computed pairwise without regard
# to the timestamps.
#
# Joseph Lee <joseph.lee@nrel.gov>


import numpy as np

class bias_pct:
    
    def compute(self,x,y):
        
        # x is baseline
        return float(np.mean(100 * (y - x) / x ))
