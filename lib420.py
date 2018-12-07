"""Classes to implement modern portfolio techniques

More comments here....
"""
import pandas as pd
import numpy as  np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
from datetime import datetime as dt
from datetime import timedelta as td
import warnings
import copy
import csv
import cvxopt
import math as m



class Asset:
    """An asset contains some info about a single security

    Attributes:
        name:
            String identifying the asset
        price_hist:
            Pandas series of historical price data
        return_hist:
            Pandas series of historical arithmetic daily return
    """
    def __init__(self, asset_name, price_hist):
        """Initialization of asset

        Args:
            asset_name: 
                Asset name (all caps, stock ticker/coin acronym)
            price_hist:
                Pandas series containing datetime and price

        """
        self.name = asset_name
        self.price_hist = price_hist
        self.return_hist = self.return_history(price_hist)

    def return_history(self,  price_hist):
        """Calculation of the arithmetic return history vector for an asset

        Args:  
            price_hist : Price history series length n

        Returns: 
            return_hist: Arithmetic return history series length n-1 

        Calculation:
                            s(d)
                  r(d) =  ________ - 1
                        
                           s(d-1)

            Where s(d) is the price of the asset on day d=0,1,...,n 
            and r(d) is defined on d=1,2,...,n
        """        
        return_hist = self.price_hist.pct_change()[1:].copy();
        return_hist.columns = ['Arithmetic Return'] 
        return return_hist

class AssetGroup():
    """Asset groups are a collection of assets and their statistical properties

    Attributes:
        assets:
            Assets objects considered in this group.
        return hist:
            Pandas DataFrame created from combination of individual asset
            return histories
        price_hist:
            DataFrame created from combination of individual asset
            price histories
        TODO: *_struct attributes? 

    Methods:
        yearly_portfolio_struct():
            Args: 
                TODO
            Returns:
                TODO
        cov_struct:
             Args: 
                TODO
            Returns:
                TODO
        cor_struct:
             Args: 
                TODO
            Returns:
                TODO
        min_volatility_alloc_struct:
            Args: 
                TODO
            Returns:
                TODO
        portfolio_volatility_struct:
            Args: 
                TODO
            Returns:
                TODO
        unlimited_frontier:
            Args: 
                TODO
            Returns:
                TODO
        long_frontier:
            Args: 
                TODO
            Returns:
                TODO
    """

    def __init__(self, *N_assets):


       
       
        
        self.assetnames  = [asset.name for asset in N_assets]

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
            # Needed b/c trading days per year may be different.. wi ll get Nan or error.. skipping catch for now

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



        # ### Calculate the base statistical properties ###z
        self.yearly_portfolio_struct()
        self.cov_struct()
        self.corr_struct()
        self.min_volatility_alloc_struct()

        

    def yearly_portfolio_struct(self):
        # asset portfolio strucutre for return histories
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
        cov_dict ={}
        for year in self.yearly_portfolio.index:
            cov_dict[year] = np.cov(self.yearly_portfolio.loc[year][0][:])
        for year in self.yearly_portfolio.index:
            cov_dict[year] = pd.DataFrame(cov_dict[year], index=self.assets, columns=self.assets)
        self.covariance_struct = copy.deepcopy(cov_dict)
    

    def corr_struct(self):
        corr_dict={}
        for year in self.yearly_portfolio.index:
            corr_dict[year] = np.corrcoef(self.covariance_struct[year])
        for year in self.yearly_portfolio.index:
            corr_dict[year] = pd.DataFrame(corr_dict[year], index=self.assets, columns=self.assets)
        self.correlation_struct = copy.deepcopy(corr_dict)
        

    # ======= ROAD TO THE FRONTIER =======
    
    def min_volatility_alloc_struct(self):#, cov_struct):
        # will compute minimum volatility portfolio allocation 
        # over all years considered or for a particular year?
        #   might be wasting time if ultimately not plotting rolling forntiers
        # whatev
        #year_cov = self.covariance_struct[]
        #y = np.linalg.solve()

        # <! -- ADD LOGIC TO HANDLE NON SEQUENTIAL CALCULATIONS OF INTERMEDIATE VALUES -->
        min_vol_dict = {}
        for year in self.yearly_portfolio.index:
            year_cov = self.covariance_struct[year]
            y = np.linalg.solve(year_cov, np.ones((year_cov.shape[0],1)))

            a = np.dot(np.ones((1,len(y))),y)
            fmv = np.dot((1/a),y.T) # should be in the order of the assets passed in 
            min_vol_dict[year] = np.ravel(fmv)
        min_vol_alloc_list = []
        for key in min_vol_dict:
            temp = np.array(min_vol_dict[key])
            min_vol_alloc_list.append(temp)
        min_volatility_allocations = pd.DataFrame(min_vol_alloc_list, index=self.yearly_portfolio.index, columns = self.assets)
        self.min_vol_allocs = min_volatility_allocations.copy()
        self.min_vol_alloc_flag = True
        return min_volatility_allocations

    def portfolio_volatility_struct(self):

        vol_list = []
        for key in self.covariance_struct.keys():
            vol = np.sqrt(np.diag(self.covariance_struct[key]))
            print(key,' ',vol)
            vol_list.append(vol)
        vol_list = np.array(vol_list)

        portfolio_vol_struct = pd.DataFrame(vol_list, index=self.yearly_portfolio.index, columns = self.assets)
        self.portfolio_volatility_struct = portfolio_vol_struct
        return portfolio_vol_struct

    
    def unlimited_frontier(self, year):
        covar = self.covariance_struct[year]
        m = []
        for asset in self.assets:
            m.append(self.return_mean_struct.loc[asset,year]["Return Mean"])
        m = np.array(m)
        y = np.ravel(np.linalg.solve(covar, np.ones((covar.shape[0],1))))
        z = np.linalg.solve(covar, m)
        a = np.dot(np.ones((1, len(y))),y)
        b = np.dot(np.ones((1, len(z))),z)
        c = np.dot(m.T, z)
        mu = np.linspace(-5e-3, 5e-3, 10000)

        sig = np.sqrt((1/a) + (a/(a*c - b**2))*(mu-(b/a))**2)
        self.unlimited_sig = sig
        self.unlimited_mu  = mu
        self.unlimited_frontier_flag  = True # successful calculation.. add logic 
        return (sig, mu)


    def long_frontier(self, year):
        covar = self.covariance_struct[year]
        m = []
        for asset in self.assets:
            m.append(self.return_mean_struct.loc[asset,year]["Return Mean"])
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
        for i in range(len(mu)):
            C1 = covar
            n  = C1.shape[1]
            C2 = np.ravel(np.zeros((1,len(covar))))
            C3 = -np.eye(len(covar))
            C4 = np.ravel(np.zeros((1,len(covar))))#zeros(length(v),1).'
            C5 = np.vstack((np.ones((1,len(covar))), [m.T])) #[ones(length(v),1).';m.']
            C6 = np.array([[1], [mu[i]]])  #[1; mu(i)]
            ######## TOOK THE TRANSPOSE OFF OF C6
            P = C1
            q = C2  #zeros(length(v),1).'
            G = C3
            h = C4
            A = C5
            b = C6

            sol = cvxopt.solvers.qp(cvxopt.matrix(P.values), cvxopt.matrix(q), cvxopt.matrix(G), cvxopt.matrix(h), cvxopt.matrix(A), cvxopt.matrix(b), solver='glpk')
            x = sol['x']
            x = np.ravel(np.array(x))
            sig[i] = np.sqrt(np.dot(np.dot(x.T,covar),x))
        print('length of sig: %d, length of mu: %d'%(len(sig), len(mu)))
        self.long_sig = sig
        self.long_mu  = mu
        self.long_front_flag = True
        return (sig, mu) 


    """
        mu = mn:.00001:mx; 
        sig  = zeros(length(mu),1);
        for i=1:1:length(mu);
        options = optimoptions('quadprog','Display','off');
        f_lf = quadprog(v,zeros(length(v),1).',-eye(length(v)),zeros(length(v),1).',[ones(length(v),1).';m.'],[1; mu(i)],[],[],[],options);
        sig(i) = sqrt(f_lf.'*v*f_lf);
        in=+1;
        end
    """ 




