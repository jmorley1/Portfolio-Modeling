"""Input/Output functions for the lib420 project


"""

import pandas as pd
from datetime import datetime as dt


def load_daily_adj_close(file_name):
    """
    Input:  Yahoo Finance CSV data. 5th column is daily adjusted close.adjusted
    Output: Price history data frame
    """
    df = pd.read_csv(file_name, usecols=[5])
    dates = []
    dateCols = pd.read_csv(file_name, usecols=[0]).values.tolist()
    for i in range(len(dateCols)):
        dates.append(dateCols[i][0])
    dates = [dt.strptime(x, '%Y-%m-%d') for x in dates]
    df.index = dates
    return df
