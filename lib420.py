
import pandas as pd
import numpy as  np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime as dt
from datetime import timedelta as td
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
        self.years = set([self.price_hist.index[i].year for i in range(len(self.price_hist))])
        
        
