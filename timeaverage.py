# IMPORTANT: THIS SCRIPT ASSUMES YOU HAVE 3X0_VARS.NC GENERATED FROM MAIN.PY
# AND LOCATED IN THE SAME FOLDER AS THIS FILE. THE VARIABLES PREC_DAILY, 
# PREC_MONTHLY, RH_DAILY, AND RH_MONTHLY WILL BE APPENDED

from netCDF4 import Dataset as ncfile
import numpy as np
from tools import calc_es, calc_rh, calc_ws, run_param, col_av
import matplotlib.pyplot as plt

#filepath = 'E:/ATM115 Data/SST300k-selected/'
filepath = './SST300k-selected/'
data3d = './SST300k-selected/sam3d.nc'
data2d = './SST300k-selected/sam2d.nc'
outputfilename = '300K_vars.nc'

sam3d = ncfile(data3d)
sam2d = ncfile(data2d)
varfile = ncfile('./300K_vars.nc','r+')

prec = sam2d['Prec'][:]
rh = varfile['rh'][:]

# Daily Averages
prec_daily = np.zeros((150,1024))
rh_daily = np.zeros((150,71,1024))

tmin = 0
tmax = 23

for day in range(0,150):
    for x in range(0,1024):
        prec_daily[day,x] = np.mean(prec[tmin:tmax,x])
        for z in range(0,71):
            rh_daily[day, z, x] = np.mean(rh[tmin:tmax,z,x])
    tmin = tmax
    tmax = tmax + 24
    print("Averaging day: " + str(day))


# Monthly Averages
prec_monthly = np.zeros((5,1024))
rh_monthly = np.zeros((5,71,1024))

tmin = 0
tmax = 30

for month in range(0,5):
    for x in range(0,1024):
        prec_monthly[month,x] = np.mean([prec_daily[tmin:tmax, x]])
        for z in range(0,71):
            rh_daily[month, z, x] = np.mean(rh_daily[tmin:tmax, z, x])
    tmin = tmax
    tmax = tmax + 30
    print("Averaging month: " + str(month))

# Write to disk
dimd = varfile.createDimension('day', 150)
dimm = varfile.createDimension('month',5)

prec_daily_out = varfile.createVariable('prec_daily', 'f4', ('day', 'x'))
rh_daily_out = varfile.createVariable('rh_daily', 'f4', ('day', 'z','x'))
prec_monthly_out = varfile.createVariable('prec_monthly', 'f4', ('month','x'))
rh_monthly_out = varfile.createVariable('prec_monthly', 'f4', ('month','z','x'))

prec_daily_out[:] = prec_daily
rh_daily_out[:] = rh_daily
prec_monthly_out[:] = prec_monthly
rh_monthly_out[:] = rh_monthly

varfile.close()