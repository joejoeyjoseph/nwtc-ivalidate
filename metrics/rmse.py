# rmse.py
#
# This is a naive root mean squared error (RMSE) calculation,
# rmse = root(mean((x - y)^2))
#
# If the input vectors differ, it takes the first N elements of each
# so that the size is the same. Error is computed pairwise without regard
# to the timestamps.
#
# Joseph Lee <joseph.lee@pnnl.gov>

import numpy as np


class rmse:

    def compute(self, x, y):

        return float(np.sqrt(np.mean((x - y)**2)))
