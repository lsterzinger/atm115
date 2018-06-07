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
