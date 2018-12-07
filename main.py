"""Executable for lib420

This is a temporary executable file so that I/O operations can be removed from the library.
"""

from lib420 import Asset
from lib420 import AssetGroup

import lib420io as io
import lib420plot as pl
from datetime import timedelta as td
from datetime import datetime as dt

### Load data and create Asset objects ###
# (All .csv files in ./Tests/ for used to test for now) #
asset_namelist = ["VBTIX","VFICX","VFINX","VGSLX","VWIGX"]
asset_list = []
for assetname in asset_namelist:
        current_asset = Asset(assetname,io.load_daily_adj_close("Tests/"+assetname+"_03_17.csv"))
        asset_list.append(current_asset)

### Plot some data about the group of assets ###

# I think this would be a good way to use an asset group. Thoughts?
assetgroup1 = AssetGroup(*asset_list)
(unlim_sig,unlim_mu) = assetgroup1.unlimited_frontier(2003)
# l.plot_test_sigma_mu(unlim_sig,unlim_mu)
