import scipy.stats as st
import numpy as np
import pandas as pd


def _as_price_series(prices):
    if isinstance(prices, pd.Series):
        return prices

    return pd.Series(prices, dtype=float)


def _as_numeric_array(values):
    return np.asarray(values, dtype=float)

def calculate_simple_returns(prices):
    price_series = _as_price_series(prices)
    return price_series.pct_change().dropna()

def calculate_log_returns(prices):
    price_series = _as_price_series(prices)
    return np.log(price_series / price_series.shift(1)).dropna()

def calculate_mean(values):
    return _as_numeric_array(values).mean()

def calculate_variance(values):
    values = _as_numeric_array(values)
    n = len(values)
    if n < 2:
        return 0.0
    return np.var(values, ddof=1)

def calculate_skewness(values):
    values = _as_numeric_array(values)
    n = len(values)
    if n < 3:
        return 0.0
    if np.allclose(values, values[0]):
        return 0.0
    return float(st.skew(values, bias=False))

def calculate_kurtosis(values):
    values = _as_numeric_array(values)
    n = len(values)
    if n < 4:
        return 0.0
    if np.allclose(values, values[0]):
        return 0.0
    return float(st.kurtosis(values, fisher=False, bias=False))

def calculate_volatility(values):
    return _as_numeric_array(values).std()

def calculate_parametric_var(returns, confidence_level, zero_mean=False):
    alpha = 1 - confidence_level
    expected_return = 0 if zero_mean else calculate_mean(returns)
    volatility = calculate_volatility(returns)
    z_score = st.norm.ppf(alpha)
    return expected_return + (volatility * z_score)

def calculate_historical_var(returns, confidence_level):
    alpha = 1 - confidence_level
    return np.percentile(returns, alpha * 100)

def calculate_monte_carlo_var(returns, confidence_level, num_simulations=10000):
    expected_return = calculate_mean(returns)
    volatility = calculate_volatility(returns)
    simulated_returns = np.random.normal(expected_return, volatility, num_simulations)
    return np.percentile(simulated_returns, (1 - confidence_level) * 100)

def calculate_parametric_cvar(returns, confidence_level):
    alpha = 1 - confidence_level
    expected_return = calculate_mean(returns)
    volatility = calculate_volatility(returns)
    z_score = st.norm.ppf(alpha)
    return expected_return - (volatility * st.norm.pdf(z_score) / alpha)

def calculate_historical_cvar(returns, confidence_level):
    alpha = 1 - confidence_level
    var_threshold = np.percentile(returns, alpha * 100)
    cvar = returns[returns <= var_threshold].mean()
    return cvar