import yfinance as yf
from MathLibrary import math_library as ml
import pandas as pd
import numpy as np
from .portfolio_asset import PortfolioAsset
from .plotter import create_risk_dashboard, plot_var_heatmap, create_optimization_dashboard

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

def run_portfolio_calculations():
    start_date = "2022-09-01"
    end_date = "2022-09-30"
    
    asset1 = PortfolioAsset("AAPL", 0.6, start_date, end_date)
    asset2 = PortfolioAsset("TSLA", 0.4, start_date, end_date)

    print("Calculating portfolio volatility from start date:", start_date, "to end date:", end_date)
    print(f"Asset 1: {asset1.name}, Weight: {asset1.weight}")
    print(f"Asset 2: {asset2.name}, Weight: {asset2.weight}")

    portfolio_risk_analyzer = PortfolioRiskAnalyzer([asset1, asset2], confidence_level=0.95)
    portfolio_volatility = portfolio_risk_analyzer.calculate_portfolio_volatility()
    print(f"Portfolio volatility: {portfolio_volatility:.4f}", end=" ")
    print_perc(portfolio_volatility)

    portfolio_hist_var = portfolio_risk_analyzer.calculate_portfolio_hist_var()
    print(f"Portfolio historical VaR: {portfolio_hist_var:.4f}", end=" ")
    print_perc(portfolio_hist_var)

    portfolio_param_var = portfolio_risk_analyzer.calculate_portfolio_param_var()
    print(f"Portfolio parametric VaR: {portfolio_param_var:.4f}", end=" ")
    print_perc(portfolio_param_var)

    portfolio_cvar = portfolio_risk_analyzer.calculate_portfolio_cvar()
    print(f"Portfolio CVaR: {portfolio_cvar:.4f}", end=" ")
    print_perc(portfolio_cvar)

    import yfinance as yf

    # 1. Pull the Market Benchmark
    spy_data = yf.download('SPY', start='2022-09-01', end='2022-10-01')['Close'].squeeze().pct_change().dropna()

    # 2. Calculate Benchmark Metrics
    spy_ret = spy_data.sum()
    spy_var = abs(np.percentile(spy_data, 5))
    spy_logic = spy_ret / spy_var

    print(f"Market (SPY) Logic: {spy_logic:.2f}")

    # create_risk_dashboard(
    #     portfolio_risk_analyzer.calculate_portfolio_weighted_returns(),
    #     initial_investment=100000
    # ).show()

    # plot_var_heatmap(
    #     portfolio_risk_analyzer.combine_asset_returns()
    # ).show()

    create_optimization_dashboard(
        portfolio_risk_analyzer.combine_asset_returns()
    ).show()

def print_perc(value):
    print(f"({value:.2%})")
