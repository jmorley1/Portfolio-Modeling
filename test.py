# file for testing library functions


import lib420 as port
import numpy as np
import pandas as pd
from datetime import datetime as dt
import matplotlib.pyplot as plt
import timeit 
import os, sys
import copy
import cvxopt

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



portfolio = port.Portfolio(VFINX, VBTIX, VGSLX, VWIGX, VFICX, VFSTX)

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
"""#print(type(pd.DataFrame(portfolio.cov_struct()[2003])))
print(pd.DataFrame(portfolio.cov_struct()[2003]))
print(type(portfolio.cov_struct()))
print(portfolio.cov_struct())
"""


"""
"""
print(portfolio.cov_struct().keys())
#print(np.corrcoef(portfolio.cov_struct()))
print(portfolio.corr_struct().keys())

print(portfolio.corr_struct()[2003])
"""
print('\n\n\n\n\n\n')
for year in portfolio.years[1:]:
	print('Covariance struct for portfolio year: %f'% year)
	print(portfolio.covariance_struct[year])

#print(type(portfolio.cov_struct()[2003]))

#print('TEST1\n\n',portfolio.covariance_struct[2003])

#print(np.portfolio.covariance_struct[2003].shape[0])

#print(portfolio.min_volatility_alloc_struct())
print(portfolio.covariance_struct[2003])
"""

a= portfolio.min_volatility_alloc_struct()
print('\n\n\n\nminimum vol alloc:\n', a)

print(portfolio.return_mean_struct)
print(type(portfolio.return_mean_struct))

print('TEEEEST\n',portfolio.covariance_struct.keys())

print('\n\n Volatility struct: \n', portfolio.portfolio_volatility_struct())
#print(np.sqrt(np.diag(portfolio.covariance_struct[2003])))


print(np.sqrt(np.diag(portfolio.covariance_struct[2003])))

#portfolio.plot_test_sigma_mu()

print(portfolio.return_mean_struct.loc["VFINX",2003]["Return Mean"])
print(portfolio.return_mean_struct.index.get_level_values(1))

#portfolio.plot_test_sigma_mu(2005)

#print('vol for 2003\n:',portfolio.portfolio_volatility_struct["VFINX"].loc[2003])

#print(portfolio.return_mean_struct["VFINX",2003]["Return Mean"])
#print(portfolio.return_mean_struct["VFINX"]["Return Mean"])
print('\n\n\n AWGE')
print(portfolio.return_mean_struct.loc['VFINX',2003]["Return Mean"], portfolio.portfolio_volatility_struct['VFINX'].loc[2003])

print('Testing structure of Minimum Volatility Structure')
print(portfolio.min_volatility_alloc_struct())
#print(portfolio.min_vol_allocs)

print(portfolio.return_mean_struct)
print(portfolio.portfolio_volatility_struct)
print(portfolio.covariance_struct[2003])


"""
sig, mu = portfolio.unlimited_frontier(2003)
print('sizes', len(mu), len(sig))

#def long_frontier(portfolio, year):
covar = portfolio.covariance_struct[year]
m = []
for asset in portfolio.assets:
	m.append(portfolio.return_mean_struct.loc[asset,year]["Return Mean"])
m = np.array(m)
mn = np.min(m)	
mx = np.max(m)

variances = np.diag(covar)
min_var   = np.min(variances)
max_var   = np.max(variances)

i = 1
mu = np.linspace(-5e-3, 5e-3, 10000)
sig = np.zeros((len(mu), 1))
#x = quadprog(C1, C2, C3, C4, C5, C6, C7, C8, ...)
#for i in range(len(mu)):
C1 = covar
n  = C1.shape[1]
C2 = np.ravel(np.zeros((1,len(covar))))
C3 = -np.eye(len(covar))
C4 = np.ravel(np.zeros((1,len(covar))))#zeros(length(v),1).'
C5 = np.vstack((np.ones((1,len(covar))), [m.T])) #[ones(length(v),1).';m.']
C6 = np.array([[1], [mu[i]]]) #[1; mu(i)]

P = C1
q = C2  #zeros(length(v),1).'
G = C3
h = C4
A = C5
b = C6

print('P')
print(P.values)
print('q')
print(q)
print('G')
print(G)
sol = cvxopt.solvers.qp(cvxopt.matrix(P.values), cvxopt.matrix(q), cvxopt.matrix(G), cvxopt.matrix(h), cvxopt.matrix(A), cvxopt.matrix(b))
x = sol['x']
print('solution:',np.ravel(np.array(x)))
print(type(x))
"""
sig, mu = portfolio.unlimited_frontier(2003)
#sig, mu = portfolio.long_frontier( 2003)
portfolio.plot_test_sigma_mu(2003)
#print(cvxopt.matrix(P))



"""
year =2003
covar = portfolio.covariance_struct[year]
m = []
for asset in portfolio.assets:
	m.append(portfolio.return_mean_struct.loc[asset,year]["Return Mean"])
m = np.array(m)
print(np.vstack((np.ones((1,len(covar))), [m.T])))

print(m.shape)


print('\n\n\n AWGE')

print(np.ravel(np.vstack(np.zeros((1,len(covar))))))
"""
#print(np.vstack(np.array([np.zeros((1,6)) , -np.eye(6), np.eye(6)])))