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
