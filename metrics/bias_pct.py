# bias_pct.py
#
# This is a simple average percent bias calculation,
# bias % = mean(100 * (y - x) / x),
# assuming x is the truth.
#
# Joseph Lee <joseph.lee@pnnl.gov>

import numpy as np


class bias_pct:

    def compute(self, x, y):

        # x is baseline
        return float(np.mean(100 * (y - x) / x))
