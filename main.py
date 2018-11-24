"""Executable for lib420

This is a temporary executable file so that I/O operations can be removed from the library.
"""

from lib420 import Asset
from lib420 import AssetGroup

import lib420io as io

from datetime import timedelta as td
from datetime import datetime as dt

### Load data and create Asset objects ###
# (All .csv files in ./Tests/ for used to test for now) #
asset_namelist = ["VBTIX","VFICX","VFINX","VGSLX","VWIGX"]
asset_list = []
for assetname in asset_namelist:
        current_asset = Asset(assetname,io.load_daily_adj_close("Tests/"+assetname+"_03_17.csv"))
        asset_list.append(current_asset)

### Create asset group with statistical data ###
data_time = td(days=1)
stat_time = td(days=252)

assetgroup1 = AssetGroup(data_time,stat_time,*asset_list)



### Plot ###
