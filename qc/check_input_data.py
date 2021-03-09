import numpy as np

def convert_mask_to_nan(var): 

    if np.ma.is_masked(var) is True: 

        var = np.NaN

    return var

        