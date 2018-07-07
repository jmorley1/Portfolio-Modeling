# file for testing library functions


import lib420 as port
import numpy as np
import pandas as pd
from datetime import datetime as dt
import timeit 
import os, sys

sys.path.append('/Users/jonnymorley/Documents/GitHub/Portfolio-Modeling/assets/')

home = os.path.expanduser("~")
sys.path.append(os.path.join(home,"Documents/Github/Portfolio-Modeling/"))
sys.path.append(os.path.join(home,"Documents/Github/Portfolio-Modeling/assets/"))
sys.path.append(home)


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

#print("Portfolio return history")
#print(portfolio.return_hist.head(),'\n')
#print("Portfolio price history")
#print(portfolio.price_hist.head())

#print(len(portfolio.return_hist_struct.loc["VFINX",2003]["Return History"]))

#print(portfolio.price_hist_struct.head())

#print(portfolio.return_mean_struct)
#test = portfolio.return_hist
#print(portfolio.return_hist["VFINX"][portfolio.return_hist["VFINX"].index])
#print(portfolio.return_hist.index.year)
'''

price

300 mionthly 
3600 *3 years

5000 painting


~ 20,000 grand.. condition 

tax deduct 18,000 taxes....__class__


avg rate 5%....  5-3%...... 7 years... 

560,0000

'''


#print(portfolio.return_hist_struct.loc["VFINX",2003]['Return History'].shape)

#print(len(np.array([portfolio.return_hist_struct.loc[asset, year]['Return History'] for asset in portfolio.assets for year in portfolio.years[1:]])[0]))

#print(portfolio.years)
#print(len(portfolio.years))
#print([portfolio.retunr_hist_struct])
#print(len(portfolio.assets))

#print(portfolio.years)
#print(len(portfolio.years[1:]))
"""
yearly_portfolio = {}
for asset in portfolio.assets:
	for year in portfolio.years[1:]:
		print(portfolio.return_hist_struct.loc[asset,year]['Return History'])
"""
yearly_portfolio = {}
for year in portfolio.years[1:]:
	port_arr = []
	print(year)
	for asset in portfolio.assets:
		port_arr.append( portfolio.return_hist_struct.loc[asset,year]['Return History'])
		print(asset)
	yearly_portfolio[year] = port_arr


print('Year return hist for portfolio for different years')
print(yearly_portfolio.keys())

#print(portfolio.return_hist_struct.loc["VFINX"].index)
#print(len([portfolio.return_hist_struct.loc[asset,year] for year in portfolio.years if asset in portfolio.assets ]))

print(len(yearly_portfolio[2006][0]))

print(portfolio.return_hist_struct.index)

print(portfolio.assets)

#temp_cov = pd.DataFrame(yearly_portfolio)
#print(temp_cov.index
print(np.array(yearly_portfolio[2003]).shape)
port_list = []
for key in yearly_portfolio.keys():
	temp = np.array(yearly_portfolio[key])
	port_list.append(temp)

print('list of 6 by num trading day matrices')
print(type(port_list))
print(len(port_list))

temp1 = pd.DataFrame(port_list)
print(temp1)
print('break')
print(temp1.iloc[0][0])
print(temp1.iloc[0][0].shape)


print(temp1.iloc[2].shape)

print(len(temp1))
print(type(temp1))
print(temp1)

print('inside')
#print(len(temp1.iloc[0]))
print(len(temp1.iloc[0][0][0]))
#print(len(temp1.iloc[0][0]))

# Verify equivalency
#print(temp1.iloc[0][0][0][:5])
#print(portfolio.return_hist_struct.loc["VFINX",2003]['Return History'][:5])

temp2 = portfolio.yearly_portfolio_struct()

print( len(temp2.iloc[0][0][:]))
print( type(temp2.iloc[0][0][:]))
print( temp2.iloc[0][0][:].shape) # confirm proper shape (6,252) for np.cov()
print(temp2.index)
print(np.cov(temp2.loc[2003][0][:]).shape)
#print(np.cov(temp2.loc[2003][0][:])[0][0])

print('\n\n\n\n')
#print(portfolio.cov_struct())
print(pd.DataFrame(portfolio.cov_struct()[2003]))


"""
"""
 
print(portfolio.return_mean_struct)



