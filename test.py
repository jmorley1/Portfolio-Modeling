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


#VFINX.price_history_plot()
#print(VFINX.price_history.head())
return_func = VFINX.return_history([0,252])

start_time = timeit.default_timer()
VFINX.return_history([0,len(VFINX.price_history)-1])
elapsed = timeit.default_timer()-start_time
print("time for my function: ",elapsed)

start_time = timeit.default_timer()
VFINX.price_history.pct_change()
elapsed = timeit.default_timer()-start_time
print("time for pandas function: ",elapsed)

print(type(VFINX.price_history))


