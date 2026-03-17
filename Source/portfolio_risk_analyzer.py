import yfinance as yf
import math_library as ml

def run_all_var_calculations(returns, confidence_level):
    parametric_var = ml.calculate_parametric_var(returns, confidence_level)
    historical_var = ml.calculate_historical_var(returns, confidence_level)
    monte_carlo_var = ml.calculate_monte_carlo_var(returns, confidence_level)
    cvar = ml.calculate_parametric_cvar(returns, confidence_level)

    print(f"Parametric VaR at {confidence_level*100}% confidence: {parametric_var:.4f}")
    print(f"Historical VaR at {confidence_level*100}% confidence: {historical_var:.4f}")
    print(f"Monte Carlo VaR at {confidence_level*100}% confidence: {monte_carlo_var:.4f}")
    print(f"CVaR at {confidence_level*100}% confidence: {cvar:.4f}")

def run_data_calculations():
    data = yf.download("AAPL", start="2020-01-01", end="2020-12-31")

    close_prices = data['Close'].squeeze()
    returns = close_prices.pct_change().dropna() 

    print("AAPL returns (head):")
    print(returns.head())

    # Set confidence level for VaR calculations
    confidence_level = 0.95
    # Run all VaR calculations
    run_all_var_calculations(returns, confidence_level)

if __name__ == "__main__":
    run_data_calculations()