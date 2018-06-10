from netCDF4 import Dataset as ncfile
import numpy as np
from tools import calc_es, calc_rh, calc_ws, col_av
import matplotlib.pyplot as plt

#filepath = 'E:/ATM115 Data/SST300k-selected/'
filepath = '/home/lsterzinger/Documents/ATM115-Data/SST300k-selected/'
data3d = '/home/lsterzinger/Documents/ATM115-Data/SST300k-selected/sam3d.nc'
data2d = '/home/lsterzinger/Documents/ATM115-Data/SST300k-selected/sam2d.nc'
outputfilename = '300K_vars.nc'

sam3d = ncfile(data3d)
sam2d = ncfile(data2d)

x = sam3d.variables['x'][:]
z = sam3d.variables['z'][:]
t = sam3d.variables['time'][:]

qv = sam3d['QV'][:]
temp = sam3d['TABS'][:]
pressure_ref = sam3d['p'][:]
pres_pert = sam3d['PP'][:]

pressure = np.zeros((3600,71,1024))
# Pressure perturbarion + base state
for i in range(0,1024):
    for j in range(0,3600):
        pressure[j,:,i] = pres_pert[j,:,i]+pressure_ref[:]
        
#Delete unneeded variables
pressure_ref = None
pres_pert = None

#Convert into celsius
temp = temp - 273.15

#Calculate e_s
es = calc_es(temp)
ws = calc_ws(pressure, es)
rh = calc_rh(qv,ws)

col_av_rh = col_av(rh, 3600, 38, 1024)

# Write everything to file
output = ncfile(outputfilename, 'w', format='NETCDF4')

#create dimensions
dimx = output.createDimension('x',len(x))
dimz = output.createDimension('z',len(z))
dimt = output.createDimension('time',len(t))

#Create variables
x_out = output.createVariable('x','f4',('x'))
z_out = output.createVariable('z','f4',('z'))
t_out = output.createVariable('time','f4',('time'))
x_out.units = 'm'
z_out.units = 'm'
t_out.units = 'days'
x_out[:] = x
z_out[:] = z
t_out[:] = t

pressure_out = output.createVariable('pressure','f4',('time','z','x'))
es_out = output.createVariable('es','f4',('time','z','x'))
rh_out = output.createVariable('rh','f4',('time','z','x'))
rh_col_out = output.createVariable('rh_col_av', 'f4', ('time','x'))
pressure_out.units = 'mb'
es_out.units = 'mb'
pressure_out[:] = pressure
es_out[:] = es
rh_out[:] = rh
rh_col_out[:] = col_av_rh

output.close()