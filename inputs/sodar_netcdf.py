# netcdf.py
#
# This is a basic parser for NetCDF data.
#
# Joseph Lee <joseph.lee@nrel.gov>

import os
import pathlib
from datetime import datetime
from netCDF4 import Dataset
import numpy as np
import pandas as pd
from qc import check_input_data

class sodar_netcdf:

  def __init__(self,path,var):
    self.path = str(pathlib.Path(os.getcwd()).parent) + '/' + str(path)
    self.var = var

  def get_ts(self,loc,lev):

    df = pd.DataFrame({"t": [], 'sodar_ws': []})

    for l in os.listdir(self.path):

      #print(l)

      ih = Dataset(self.path + "/" + l, 'r')

      #s = '_'.join(ih['time'].units.split(' ')[2:4])
      s = '_'.join(l.split('.')[3:5])
      t = datetime.strptime(s, "%Y%m%d_%H%M%S")

      #level = 3
      height_ind = np.where(ih['height'][:].data == lev)[0][0]
      #print(height_ind)
      ws = ih.variables[self.var][0][height_ind]

      # # sodar data were masked at 2016-09-23 16:10 and 16:20
      # if np.ma.is_masked(ws) is True: 
      #     ws = np.NaN

      ws = check_input_data.convert_mask_to_nan(ws)

      ih.close()
      df = df.append([{"t": t, 'sodar_ws': ws}])

      #print('done')

    df = df.set_index("t").sort_index()

    return df