# Price a European option by the binomial tree model

from StockOption import StockOption
import math
import numpy as np

class BinomialEuropeanOption(StockOption):

    def __setup_parameters__(self):
        """ Required calculations for the model """
        self.M = self.N + 1  # Number of terminal nodes of tree
        self.u = 1 + self.pu  # Expected value in the up state
        self.d = 1 - self.pd  # Expected value in the down state
        self.qu = (math.exp((self.r - self.div) * self.dt) - self.d) / (self.u - self.d)
        self.qd = 1 - self.qu

    def _initialize_stock_price_tree_(self):
        """ Initialize terminal price nodes to zeros and calculate expected stock prices for each node """
        self.STs = np.zeros(self.M)  # Directly assign an array to STs
        for i in range(self.M):
            self.STs[i] = self.S0 * (self.u ** (self.N - i)) * (self.d ** i)

    def _initialize_payoffs_tree_(self):
        """ Get payoffs when the option expires at terminal nodes """
        payoffs = np.maximum(
            0, (self.STs - self.K) if self.is_call
            else (self.K - self.STs)
        )
        return payoffs

    def _traverse_tree_(self, payoffs):
        """ Traverse the tree backwards and calculate discounted payoffs at each node """
        for i in range(self.N):
            payoffs = (payoffs[:-1] * self.qu + payoffs[1:] * self.qd) * self.df
        return payoffs

    def __begin_tree_traversal__(self):
        "sssss"" Start tree traversal """
        payoffs = self._initialize_payoffs_tree_()
        return self._traverse_tree_(payoffs)

    def price(self):
        """ The pricing implementation """
        self.__setup_parameters__()
        self._initialize_stock_price_tree_()
        payoffs = self.__begin_tree_traversal__()
        return payoffs[0]  # Option value converges to first node
