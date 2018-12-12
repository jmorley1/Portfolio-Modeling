"""
lib420 Workflow test script
"""

from lib420 import Asset
from lib420 import AssetGroup
import lib420io as io
import lib420plot as apl 
import datetime as dt

import matplotlib.pyplot as plt

# 'apl : asset plot'
# Not to be confused with 'plt'
# Which is commonly reserved for matplotlib.pyplot

print("TEST @ ", dt.datetime.today(), '\n')

# Load data and create Asset objects (located in ./Tests)
asset_namelist = ["VBTIX", "VFICX", "VFINX", "VGSLX", "VWIGX"]
asset_list = []



for assetname in asset_namelist:
    asset = Asset(assetname,io.load_daily_adj_close("Tests/"+assetname+"_03_17.csv"))
    asset_list.append(asset)

# Create and initialize AssetGroup Object
assetGroup = AssetGroup(*asset_list)


'''
Price history for each asset:  2003 - 2018
To disscretize time, perhaps use rigid UI elements
to constrain data selection choices.print
i.e.: Input text field for "Asset Ticker"
      Drop down scroll menu revealing years
      for starting and ending periods <2003> - <2017>
      Makes defining and fetching day 0 easier as well.
This provides an elegant way of restricting selection
To Be Continued.
'''

print("Asset Group Price History Structure:")
print(assetGroup.price_hist.head())
print("Price Hist Shape (Dates x Assets):", assetGroup.price_hist.shape, '\n')

print("Asset Group Return History Structure:")
print(assetGroup.return_hist.head())
print("Return Hist Shape (DatesxAssets):", assetGroup.return_hist.shape, '\n')


# Demonstrate how to index return history DataFrame

print("First element of return history for VFINX:")
print(assetGroup.return_hist["VFINX"][0], '\n')

# Indices of price and return history data frames
# are natively a type of date-time object
print("Data frame index types:")
print(type(assetGroup.return_hist["VFINX"].index), '\n')

# To retrieve view of specific asset/year of return history dataframe:
print("How many days did VFINX trade in 2003?:")
print(len(assetGroup.return_hist_struct.loc["VFINX",2003]["Return History"]), '\n')

# To retrieve a view of all return history of an asset in 
# return history data frame: (commented out b/c 3776 elements long)
# print(portfolio.return_hist["VFINX"][portfolio.return_hist["VFINX"].index])

# The return mean data frame uses multidimensional indexing
# Uncomment line below to view structure
#print(assetGroup.return_mean_struct) 

# Retrieve a view of return mean for an asset/year pair
print("What was the return mean of VBTIX in 2003: ")
print(assetGroup.return_mean_struct.loc["VBTIX",2003]["Return Mean"], '\n')
# For all years of an asset
#print(portfolio.return_mean_struct["VFINX"]["Return Mean"])

print('Minimum Volatility Allocations by year, for the group (head):')
print(assetGroup.min_volatility_alloc_struct().head(), '\n')


# **** What does this do??
#groupVolatilityStruct = assetGroup.portfolio_volatility_struct()
#print(assetGroup.portfolio_volatility_struct)
#print(assetGroup.covariance_struct[2003])

# Need to work on plotting stuff
# Thought: by separating into another separate
# module, there is no native access to AssetGroup
# attributes on the fly. Might be faster/cleaner
# to keep plotting functions in lib420. 
# originally implemented pretty off the cuff like
# but it can be cleaned up and made modular 

sig, mu = assetGroup.unlimited_frontier(2003)
#sig, mu = portfolio.long_frontier( 2003)
#assetGroup.plot_test_sigma_mu(2003)
plt.plot(sig,mu); plt.title('Unlimited Frontier of AssetGroup: 2003')
plt.xlabel('mu');plt.ylabel('sigma')
plt.show()