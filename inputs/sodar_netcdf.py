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

target_var = 'sodar_ws'

class sodar_netcdf:

  def __init__(self,path,var):
    self.path = str(pathlib.Path(os.getcwd()).parent) + '/' + str(path)
    self.var = var

  def get_ts(self,loc,lev, freq):

    df = pd.DataFrame({"t": [], target_var: []})

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

      ws = check_input_data.convert_mask_to_nan(ws)

      ih.close()
      df = df.append([{"t": t, target_var: ws}])

      #print('done')

    df = df.set_index("t").sort_index()

    check_input_data.verify_data_file_count(df, target_var, self.path, freq)

    # print(df.index.min())
    # print(df.index.max())
    
    # diff_sec = (df.index.max() - df.index.min()).total_seconds() / 60.0

    # print('read in '+target_var+' from '+str(df.index.min())+' to '+str(df.index.max()))

    # if len(os.listdir(self.path)) == (diff_sec + freq) / freq: 
    #   print('good')


    # print(freq)

    return df