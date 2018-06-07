from netCDF4 import Dataset as ncfile
import numpy as np
import matplotlib.pyplot as plt

filepath = 'E:/ATM115 Data/SST300k-selected/'
filename = 'sam3d.nc'

sam3d = ncfile(filepath+filename)

x = sam3d.variables['x'][:]
z = sam3d.variables['z'][:]
t = sam3d.variables['time'][:]

