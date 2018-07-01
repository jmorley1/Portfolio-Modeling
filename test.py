# file for testing library functions


import lib420 as port
import numpy as np
import pandas as pd
from datetime import datetime as dt
import timeit 
"""price_hist = port.load_daily_adj_close("VFINX_03_17.csv")

print(price_hist.head())


# trading day indices [1 253; 253 505; 505 757 ...] from matlab.. note proper indexing from zero

trading_day_indices = [[0, 252],[253, 505]] """
VFINX = port.Asset("VFINX","VFINX_03_17.csv")
VBTIX = port.Asset("VBTIX","VBTIX_03_17.csv")
VGSLX = port.Asset("VGSLX","VGSLX_03_17.csv")
VFSTX = port.Asset("VFSTX","VFSTX_03_17.csv")
VFICX = port.Asset("VFICX","VFICX_03_17.csv")
VWIGX = port.Asset("VWIGX","VWIGX_03_17.csv")

#Data Format Check: VFINX.price_history_plot()
#Data Format Check: print(VFINX.price_history.head())
# Version 2 test:  return_func = VFINX.return_history([0,252])

""" Speed tests for V1 and V2 of tested funcs
start_time = timeit.default_timer()
VFINX.return_history([0,len(VFINX.price_history)-1])
elapsed = timeit.default_timer()-start_time
print("time for my function: ",elapsed)

start_time = timeit.default_timer()
VFINX.price_history.pct_change()
elapsed = timeit.default_timer()-start_time
print("time for pandas function: ",elapsed)

"""

#print(VFINX.return_history().head())
#print(VFINX.return_history().tail())

#print(len(VFINX.return_history()))
#VFINX.price_history_plot()


portfolio = port.Portfolio(VFINX, VBTIX, VGSLX, VFSTX, VFICX, VWIGX)

#print(portfolio.return_hist.shape) 

print("Portfolio return history")
print(portfolio.return_hist.head(),'\n')
#print("Portfolio price history")
#print(portfolio.price_hist.head())

print(len(portfolio.return_hist_struct.loc["VFINX",2003]["Return History"]))

print(portfolio.price_hist_struct.head())

print(portfolio.return_mean_struct)

