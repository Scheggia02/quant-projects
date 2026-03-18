import yfinance as yf
import numpy as np
from MathLibrary import math_library as ml

from PortfolioRiskAnalyzer.portfolio_asset import PortfolioAsset
from PortfolioRiskAnalyzer.portfolio_risk_analyzer import PortfolioRiskAnalyzer
from .plotter import create_risk_dashboard, plot_var_heatmap, create_optimization_dashboard

def print_perc(value):
    print(f"({value:.2%})")

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

    # # 1. Pull the Market Benchmark
    spy_asset = PortfolioAsset("SPY", 0, start_date, end_date)
    spy_data = spy_asset.returns["return"].values

    # # 2. Calculate Benchmark Metrics
    spy_var = abs(ml.calculate_historical_var(spy_data, 0.95))
    spy_logic = spy_data.sum() / spy_var

    print(f"Market (SPY) Logic: {spy_logic:.2f}")

    # create_risk_dashboard(
    #     portfolio_risk_analyzer.calculate_portfolio_weighted_returns(),
    #     initial_investment=100000
    # ).show()

    # plot_var_heatmap(
    #     portfolio_risk_analyzer.combine_asset_returns()
    # ).show()

    #create_optimization_dashboard(
    #    portfolio_risk_analyzer.combine_asset_returns()
    #).show()