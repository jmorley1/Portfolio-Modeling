"""Executable for lib420

This is a temporary executable file so that I/O operations can be removed from the library.
"""

import lib420





def load_daily_adj_close(self, file_name):
        """ 
        Input:  Yahoo Finance CSV data. 5th column is daily adjusted close.adjusted
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