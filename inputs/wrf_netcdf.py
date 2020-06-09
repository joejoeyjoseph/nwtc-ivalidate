# netcdf.py
#
# This is a basic parser for NetCDF data.
#
# This input parser expects to be given a directory filled with netcdf files - each a grid at one particular time
# we expect that the file has a field called XLAT which is a matrix of latitude values for the grid and
# XLONG which is a matrix of longitude values for the grid.
#
# Caleb Phillips <caleb.phillips@nrel.gov>

import os
from datetime import datetime
from netCDF4 import Dataset
import numpy as np
import pandas as pd

class wrf_netcdf:

  def __init__(self,path,var):
    self.path = path
    self.var = var

  def get_ij(self,ih,loc):
    lat = np.array(ih["XLAT"][0])
    lon = np.array(ih["XLONG"][0])
    # if lat/lon were arrays (instead of matrixes) something like this would work:
    #d = np.fromfunction(lambda x,y: (lon[x] - loc["lon"])**2 + (lat[y] - loc["lat"])**2, (len(lon), len(lat)), dtype=float)
    d = (lat - loc["lat"])**2 + (lon - loc["lon"])**2
    i,j = np.unravel_index(np.argmin(d),d.shape)
    return (i,j)

  def get_ts(self,loc):
    df = pd.DataFrame({"t": [], self.var: []})
    for l in os.listdir(self.path):
      ih = Dataset(self.path + "/" + l, 'r')
      i,j = self.get_ij(ih,loc)
      # print(i,j)
      # print('hi')
      # print(ih.variables["Times"])
      # print(str(ih.variables["Times"][0]))
      # print('hey')
      # a1 = ih.variables["Times"][0][0].decode("utf-8")
      # print(a1)
      s = "".join(map(bytes.decode, ih.variables["Times"][0]))
      #a = "".join(ih.variables["Times"][0].decode("utf-8"))
      print(s)
      #t = datetime.strptime("".join(str(ih.variables["Times"][0])),"%Y-%m-%d_%H:%M:%S")
      t = datetime.strptime(s, "%Y-%m-%d_%H:%M:%S")
      v = ih.variables[self.var][0][i][j]
      ih.close()
      df = df.append([{"t":t, self.var:v}])

    df = df.set_index("t").sort_index()
    return df
