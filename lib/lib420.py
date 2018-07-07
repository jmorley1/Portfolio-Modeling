
import pandas as pd
import numpy as  np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime as dt
from datetime import timedelta as td
import warnings
import csv


class Asset:

    def __init__(self, asset_name, file_name):
        self.name = asset_name
        self.price_hist = self.load_daily_adj_close(file_name)
        self.return_hist = self.return_history()



    def load_daily_adj_close(self, file_name):
        """ Input:  Yahoo Finance CSV data. 5th column is daily adjusted close.adjusted
        Output: Price history data frame """
        df = pd.read_csv(file_name,usecols=[5])
        dates = []
        temp = pd.read_csv(file_name,usecols=[0]).values.tolist()
        for i in range(len(temp)):
            dates.append(temp[i][0])
        dates = [dt.strptime(x,'%Y-%m-%d') for x in dates]
        df.index = dates
        self.price_hist = df
        return df.copy()

    #******** TODO: Date scraping from csv data and other crypto source to feed into
    #********       return history function for some time span

    def return_history(self):  # num_trading_days):
        """ Input:  Price history data frame and number of trading days in time span
                    num_trading_days shape: [1 253; 254 505; ...]
            Output: Arithmetic return history  r(d) = [s(d)/s(d-1)]-1"""
        
        # VERSION1: Older-slower code:
        """span = np.arange(num_trading_days[0],num_trading_days[1]+1) # one extra for day 0
        return_hist = np.ones(num_trading_days[1]-num_trading_days[0])
        for i in range(len(return_hist)):
        return_hist[i] = (self.price_history.iloc[span[i]+1] - self.price_history.iloc[span[i]])/ self.price_history.iloc[span[i]]
        return pd.DataFrame(return_hist, columns=["Simple Return History"]) """
        
        # VERSION 2: Newer-Faster Code:  1600x faster
        #return self.price_history[num_trading_days[0]:num_trading_days[1]+1].pct_change()

        #VERSION 3: Eliminates the num_trading_days arg to accommodate object slicing convention
        temp = self.price_hist.pct_change()[1:].copy(); #first value will be Nan b/c day zero
        temp.columns = ['Arithmetic Return']
        return temp

    def price_history_plot(self):
        """ TODO: make display better """
        #years    = mdates.YearLocator()
        #months   = mdates.MonthLocator()
        #yearsFmt = mdates.DateFormatter('%Y')
        fig, ax = plt.subplots()
        #ax.plot(range(len(self.price_history)),self.price_history)
        ax.plot(self.price_hist.index, self.price_hist)
        plt.xlabel("Day in Trading Period")
        plt.ylabel("Asset Price ($)")
        plt.grid()
        plt.show()


class Portfolio():
    def __init__(self, *N_assets, ):
    	# first arg catches comma separated asset objects, 
        self.return_hist = pd.DataFrame([asset.return_hist['Arithmetic Return'].values for asset in  N_assets],
                                        index=[asset.name for asset in N_assets],
                                        columns=N_assets[0].return_hist['Arithmetic Return'].index.values).T
        self.price_hist = pd.DataFrame([asset.price_hist['Adj Close'].values for asset in  N_assets],
                                        index=[asset.name for asset in N_assets],
                                        columns=N_assets[0].price_hist['Adj Close'].index.values).T 
        self.years = sorted(list(set([self.price_hist.index[i].year for i in range(len(self.price_hist))])))
        self.assets  = [asset.name for asset in N_assets]
        self.return_hist_struct =  pd.DataFrame([[ self.return_hist[asset][ self.return_hist.index.year == year].values] for asset in self.assets for year in self.years ],
             							index = pd.MultiIndex.from_tuples([(asset,year) for asset in self.assets for year in self.years]),
             							columns=["Return History"],
             							dtype='float64').sort_index(level=0)
        	# returns dtype: "object"... must unpack when referencing an asset and year by ["Return History"]
        	# EX: portfolio.return_hist_struct.loc["VFINX",2003]["Return History"]
        	# Needed b/c trading days per year may be different.. will get Nan or error.. skipping catch for now

        self.price_hist_struct =  pd.DataFrame([[ self.price_hist[asset][ self.price_hist.index.year == year].values] for asset in self.assets for year in self.years ],
             							index = pd.MultiIndex.from_tuples([(asset,year) for asset in self.assets for year in self.years]),
             							columns=["Price History"],
             							dtype='float64').sort_index(level=0)
        	#EX: portfolio.price_hist_struct.loc["VINFX",2003]["Price History"]
        with warnings.catch_warnings():
        	warnings.simplefilter("ignore")
        	self.return_mean_struct = pd.DataFrame([[ np.mean(self.return_hist[asset][ self.return_hist.index.year == year].values)] for asset in self.assets for year in self.years ],
                                        index = pd.MultiIndex.from_tuples([(asset,year) for asset in self.assets for year in self.years]),
                                        columns=["Return Mean"],
                                        dtype='float64').dropna().sort_index(level=0)
 			# Run time warning b/c 
        	# /anaconda3/lib/python3.6/site-packages/numpy/core/_methods.py:80: RuntimeWarning: invalid value encountered in double_scalars
  			# ret = ret.dtype.type(ret / rcount)
			# /anaconda3/lib/python3.6/site-packages/numpy/core/fromnumeric.py:2957: 
			# RuntimeWarning: Mean of empty slice. out=out, **kwargs)
        
        	# Drop the Nan columns for the year index with one input
        	# in the return struct the zero day year should be deleted.

    def yearly_portfolio_struct(self):
    	portfolio_dict = {}
    	for year in self.years[1:]:
    		portfolio_for_year = []
    		for asset in self.assets:
    			portfolio_for_year.append(self.return_hist_struct.loc[asset,year]['Return History'])
    		portfolio_dict[year] = portfolio_for_year
    	port_list = []
    	for key in portfolio_dict.keys():
    		temp = np.array(portfolio_dict[key])
    		port_list.append(temp)
    	self.yearly_portfolio = pd.DataFrame(port_list, index=self.years[1:], columns=['Portfolio'])
    	return self.yearly_portfolio
    	    	# Returns a data frame with indices equal to years except for the year with one day used for day zero
    	# One column. Each sub element is a list with X number of return histories equal to number of assets in port
    	# The sequence in the 
    	# type(temp1.iloc[0]) -> pandas series
    	# type(temp1.iloc[0][0] -> (np array) required to access.. one element list of lists... change later using ravel)
    	# type(temp1.iloc[i][0][j] -> np ndarray,  yields return history for the asset (j) for year (i) )
    	# The sequence for index [j] is the sequence of assets as loaded into the portfolio class constructor
    	# therefore for 6 elements loaded in, index [5] corresponds to the last asset..

    # Consider adding these back to init...
    def cov_struct(self):

    	cov_dict = {}
    	for year in self.yearly_portfolio.index:
    		cov_dict[year] = np.cov(self.yearly_portfolio.loc[year][0][:])
    	#covariance_struct = pd.DataFrame(cov_dict) # figure out how to put in data frame
    	# (6x6) x 15 years not doable with simple assignment... keep dict?
    	return cov_dict #covariance_struct

""" Rolling efficient frontiers... set a calibration window that is 352 days long
    clibrate model on this window... plot frontiers continuously..
    have them evolve smoothly"""

    


