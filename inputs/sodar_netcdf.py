# netcdf.py
#
# This is a basic parser for NetCDF data.
#
# Joseph Lee <joseph.lee@pnnl.gov>

import os
import pathlib
from datetime import datetime
from netCDF4 import Dataset
import numpy as np
import pandas as pd

from qc import check_input_data


class sodar_netcdf:

    def __init__(self, path, var, target_var):

        self.path = str(pathlib.Path(os.getcwd()).parent)+'/'+str(path)
        self.var = var
        self.target_var = target_var

    def get_ts(self, lev, freq, flag):

        df = pd.DataFrame({'t': [], self.target_var: []})

        # to print an empty line before masked value error messages
        mask_i = 0

        for file in os.listdir(self.path):

            data = Dataset(self.path+'/'+file, 'r')

            s = '_'.join(file.split('.')[3:5])
            t = datetime.strptime(s, '%Y%m%d_%H%M%S')

            height_ind = np.where(data['height'][:].data == lev)[0][0]

            ws = data.variables[self.var][0][height_ind]

            ws, mask_i = check_input_data.convert_mask_to_nan(ws, t, mask_i)
            ws = check_input_data.convert_flag_to_nan(ws, flag, t)

            data.close()
            df = df.append([{'t': t, self.target_var: ws}])

        df = df.set_index('t').sort_index()

        df = check_input_data.verify_data_file_count(df, self.target_var,
                                                     self.path, freq
                                                     )

        return df
