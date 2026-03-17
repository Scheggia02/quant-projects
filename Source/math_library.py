import scipy.stats as st
import numpy as np

def calculate_volatility(values):
    return values.std()

def calculate_parametric_var(returns, confidence_level):
    alpha = 1 - confidence_level
    expected_return = returns.mean()
    volatility = calculate_volatility(returns)
    z_score = st.norm.ppf(alpha)
    return expected_return + (volatility * z_score)

def calculate_historical_var(returns, confidence_level):
    alpha = 1 - confidence_level
    return np.percentile(returns, alpha * 100)

def calculate_monte_carlo_var(returns, confidence_level, num_simulations=10000):
    expected_return = returns.mean()
    volatility = calculate_volatility(returns)
    simulated_returns = np.random.normal(expected_return, volatility, num_simulations)
    return np.percentile(simulated_returns, (1 - confidence_level) * 100)

def calculate_parametric_cvar(returns, confidence_level):
    alpha = 1 - confidence_level
    expected_return = returns.mean()
    volatility = calculate_volatility(returns)
    z_score = st.norm.ppf(alpha)
    return expected_return - (volatility * st.norm.pdf(z_score) / alpha)

def calculate_historical_cvar(returns, confidence_level):
    alpha = 1 - confidence_level
    var_threshold = np.percentile(returns, alpha * 100)
    cvar = returns[returns <= var_threshold].mean()
    return cvar