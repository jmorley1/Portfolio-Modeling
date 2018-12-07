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


#==== PLOTTING AND SUPPORT =======

# this will plot asset mean and volatility in the sigma- Mu plane
#   - later make this more aware/dynamic, 
#           - should know if other plots are open and 
#             have opportunity to add to the existing plot
# is there a way to set a global fig that can be queried on the fly?
def plot_test_sigma_mu(self, year):

    fig = plt.figure()
    
    spec  = gridspec.GridSpec(ncols=1, nrows=1)
    ax1 = fig.add_subplot(spec[0,0])

    means = []; vols = [];
    for asset in self.assets:
        #for year in self.years[1:]:
        #means.append(self.return_mean_struct.loc[asset,year]["Return Mean"])
        #vols.append(self.portfolio_volatility_struct[asset].loc[year])
        mean = self.return_mean_struct.loc[asset,year]["Return Mean"]
        vol = (self.portfolio_volatility_struct[asset].loc[year])
        #plt.plot(means, vols, 'o')
        plt.plot(vol, mean, 'o')
        plt.annotate(asset, xy=(vol,mean))

    if self.unlimited_frontier_flag:
        plt.plot(self.unlimited_sig, self.unlimited_mu)
    #if self.long_front_flag:
    #plt.plot(self.long_sig, self.long_mu)




    #plt.annotate(asset, xy=zip(vols))
    plt.title('Return means and Volatities in $\sigma-\mu$:  %d'%year)
    plt.ylabel('Return Mean $\mu$')
    plt.xlabel('Volatility $\sigma$')
    plt.grid()
    plt.show()
    return #(means, vols)
"""
def plot_unlimited_frontier(self):
    ax = plt.gca()
    ax.plot(self.unlimited_sig, self.unlimited_mu)

    """



