import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime as dt
from datetime import timedelta as td
import pandas as pd
import numpy as  np
import urllib.request
import json
import csv
import os

# API SOURCE: https://min-api.cryptocompare.com/

class Asset:

    def __init__(self, asset_name):
        #self.name = asset_name
        #self.price_hist = self.load_daily_adj_close(file_name)
        #self.return_hist = self.return_history()
