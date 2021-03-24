# mae_pct.py
#
# This is a simple average percent absolute error calculation,
# mae % = mean(100 * |x - y| / x),
# assuming x is the truth.
#
# Joseph Lee <joseph.lee@pnnl.gov>

import numpy as np


class mae_pct:

    def compute(self, x, y):

        # float(np.mean(100 * abs(np.array(x) - np.array(y)) / np.array(x) ))

        return float(np.mean(100 * np.ma.masked_invalid(abs(x - y) / x)))
