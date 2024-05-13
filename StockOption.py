import math
from typing import Dict, Optional, List


class StockOption:
    S0: float  # Initial stock price
    K: float  # Strike price
    r: float  # Risk-free rate per annum
    T: float  # Maturity per year
    N: int  # Number of time steps
    STs: Optional[List[float]]  # Stock prices tree
    pu: float  # Probability of up state
    pd: float  # Probability of down state
    div: float  # Dividend yield
    sigma: float  # Volatility
    is_call: bool  # True for call option, False for put option
    is_european: bool  # True for European option, False for American option
    dt: float  # Single time step, in years
    df: float  # Discount factor

    def __init__(self, S0: float, K: float, r: float, T: float, N: int, params: Dict[str, float]):
        self.S0 = S0
        self.K = K
        self.r = r
        self.T = T
        self.N = max(1, N)
        self.STs = None
        
        self.pu = params.get("pu", 0)
        self.pd = params.get("pd", 0)
        self.div = params.get("div", 0)
        self.sigma = params.get("sigma", 0)
        self.is_call = params.get("is_call", True)
        self.is_european = params.get("is_eu", True)

        self.dt = T / float(N)
        self.df = math.exp(-(r - self.div) * self.dt)
