# netcdf.py
#
# This is a basic parser for NetCDF data.
#
# This input parser expects to be given a directory filled with netcdf files - each a grid at one particular time
# we expect that the file has a field called XLAT which is a matrix of latitude values for the grid and
# XLONG which is a matrix of longitude values for the grid.
#
# Caleb Phillips <caleb.phillips@nrel.gov>
# Joseph Lee <joseph.lee@nrel.gov>

import os
import pathlib
from datetime import datetime
from netCDF4 import Dataset
import numpy as np
import pandas as pd
from qc import check_input_data

class wrf_netcdf:

  def __init__(self,path,var, target_var):

    self.path = str(pathlib.Path(os.getcwd()).parent) + '/' + str(path)
    self.var = var
    self.target_var = target_var

  def get_ij(self,ih,loc):

    lat = np.array(ih["XLAT"][0])
    lon = np.array(ih["XLONG"][0])
    #print(lat)
    # if lat/lon were arrays (instead of matrixes) something like this would work:
    #d = np.fromfunction(lambda x,y: (lon[x] - loc["lon"])**2 + (lat[y] - loc["lat"])**2, (len(lon), len(lat)), dtype=float)
    d = (lat - loc["lat"])**2 + (lon - loc["lon"])**2
    i,j = np.unravel_index(np.argmin(d),d.shape)

    return (i,j)

  def get_ts(self,loc):

    df = pd.DataFrame({"t": [], self.var: []})

    for l in os.listdir(self.path):

      ih = Dataset(self.path + "/" + l, 'r')
      #print(ih.variables)
      i,j = self.get_ij(ih,loc)
      s = "".join(map(bytes.decode, ih.variables["Times"][0]))
      t = datetime.strptime(s, "%Y-%m-%d_%H:%M:%S")
      print(t)
      v = ih.variables[self.var][0][i][j]
      print(v)
      ih.close()
      df = df.append([{"t":t, self.var:v}])

    df = df.set_index("t").sort_index()

    return df

  ### for WRF MW case (extracted from Eagle) ###

  def get_var_ij(self,ih,loc):

    lat = np.array(ih["XLAT"])
    lon = np.array(ih["XLONG"])
    #print(lat)
    # if lat/lon were arrays (instead of matrixes) something like this would work:
    #d = np.fromfunction(lambda x,y: (lon[x] - loc["lon"])**2 + (lat[y] - loc["lat"])**2, (len(lon), len(lat)), dtype=float)
    d = (lat - loc["lat"])**2 + (lon - loc["lon"])**2
    i,j = np.unravel_index(np.argmin(d),d.shape)

    return (i,j)

  def get_var_ts(self,loc,lev, freq, flag):

    df = pd.DataFrame({"t": [], self.target_var: []})

    mask_i = 0

    for l in os.listdir(self.path):

      ih = Dataset(self.path + "/" + l, 'r')
      i,j = self.get_var_ij(ih,loc)

      s = l.split('_')[2]+'_'+l.split('_')[3].split('.')[0]+':'\
          +l.split('_')[4]+':'+l.split('_')[5].split('.')[0]
      t = datetime.strptime(s, "%Y-%m-%d_%H:%M:%S")

      #level = 3
      height_ind = np.where(ih['level'][:].data == lev)[0][0]
      #print(height_ind)
      u = ih.variables[self.var[0]][height_ind][i][j]
      v = ih.variables[self.var[1]][height_ind][i][j]
      ws = np.sqrt(u**2 + v**2)

      ws, mask_i = check_input_data.convert_mask_to_nan(ws, t, mask_i)
      ws = check_input_data.convert_flag_to_nan(ws, flag, t)

      ih.close()
      df = df.append([{"t": t, self.target_var: ws}])

    df = df.set_index("t").sort_index()

    df = check_input_data.verify_data_file_count(df, self.target_var, self.path, freq)

    return df
