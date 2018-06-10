from math import pi, exp, pow
import numpy as np 


def calc_es(temperature):
    es = 6.11*np.power(10, (7.5*temperature)/(237.3+temperature))
    return es


def calc_ws(pressure, es):
    ws = 621.97*(es/(pressure-es))
    return ws


def calc_rh(w, ws):
    rh = w/ws
    return rh


def col_av(variable, tmax, zmax, xmax):
    col_av_var = np.zeros((tmax, xmax))
    for t in range(0, tmax):
        for x in range(0, xmax):
            col_av_var[t,x] = np.average(variable[t,0:zmax,x])
    return col_av_var


def run_param(rh):
    p = np.exp(15.6*(rh-0.603))
    return p