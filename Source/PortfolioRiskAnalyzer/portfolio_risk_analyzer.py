from MathLibrary import math_library as ml
import pandas as pd
import numpy as np

class PortfolioRiskAnalyzer:
    def __init__(self, assets, confidence_level):
        self.assets = assets
        self.confidence_level = confidence_level

        assert np.isclose(sum(asset.weight for asset in self.assets), 1.0), "Total weight of assets must equal 1."
        assert self.confidence_level > 0 and self.confidence_level < 1, "Confidence level must be between 0 and 1."
    
    def combine_asset_returns(self):
        asset_return_series = [
            asset.returns.set_index("date")["return"].rename(asset.name)
            for asset in self.assets
        ]
        returns_df = pd.concat(asset_return_series, axis=1, join='inner')
        return returns_df
    
    def calculate_portfolio_weights(self):
        return np.array([asset.weight for asset in self.assets])

    def calculate_portfolio_weighted_returns(self):
        returns_df = self.combine_asset_returns()
        weights = self.calculate_portfolio_weights()
        portfolio_returns = returns_df.dot(weights)
        return portfolio_returns

    def calculate_portfolio_volatility(self):
        portfolio_cov = self.combine_asset_returns().cov().to_numpy()
        weights = self.calculate_portfolio_weights()
        portfolio_variance = weights @ portfolio_cov @ weights
        return np.sqrt(portfolio_variance)

    def calculate_portfolio_hist_var(self):
        portfolio_returns = self.calculate_portfolio_weighted_returns()
        return -ml.calculate_historical_var(portfolio_returns, self.confidence_level)

    def calculate_portfolio_param_var(self):
        portfolio_returns = self.calculate_portfolio_weighted_returns()
        return -ml.calculate_parametric_var(portfolio_returns, self.confidence_level)

    def calculate_portfolio_cvar(self):
        portfolio_returns = self.calculate_portfolio_weighted_returns()
        return -ml.calculate_parametric_cvar(portfolio_returns, self.confidence_level)


