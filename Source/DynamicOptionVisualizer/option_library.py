import numpy as np
import scipy.stats as stats

def calculate_d1_term(S, K, T, r, sigma):
    return (np.log(S / K) + (r + (sigma**2) * 0.5) * T) / (sigma * np.sqrt(T))

def calculate_d2_term(d1, sigma, T):
    return d1 - (sigma * np.sqrt(T))

def calculate_black_scholes(S, K, T, r, sigma):
    d1 = calculate_d1_term(S, K, T, r, sigma)
    d2 = calculate_d2_term(d1, sigma, T)

    return S * stats.norm.cdf(d1) - K * np.exp(-r * T) * stats.norm.cdf(d2)

def calculate_delta(S, K, T, r, sigma):
    d1 = calculate_d1_term(S, K, T, r, sigma)
    return stats.norm.cdf(d1)

def calculate_gamma(S, K, T, r, sigma):
    d1 = calculate_d1_term(S, K, T, r, sigma)
    return stats.norm.pdf(d1) / (S * sigma * np.sqrt(T))

def calculate_theta(S, K, T, r, sigma):
    d1 = calculate_d1_term(S, K, T, r, sigma)
    d2 = calculate_d2_term(d1, sigma, T)

    numerator = S * stats.norm.pdf(d1) * sigma
    denominator = 2 * np.sqrt(T)
    return -(numerator / denominator) - r * K * np.exp(-r * T) * stats.norm.cdf(d2)

def calculate_vega(S, K, T, r, sigma):
    d1 = calculate_d1_term(S, K, T, r, sigma)
    return S * np.sqrt(T) * stats.norm.pdf(d1)

def calculate_volatility_surface(S, K, base_vol, skew, smile):
    # Moneyness is the log of the ratio of spot price to strike price, how far is the spot from the strike.
    moneyness = np.log(S / K)
    # The volatility surface is modeled as a quadratic function of moneyness, with parameters for the base level, skew, and smile.
    iv_surface = base_vol + skew * moneyness + smile * (moneyness ** 2)
    
    return np.maximum(iv_surface, 0.01)  # Ensure volatility is not negative, set a floor of 1%

def calculate_bs_metrics(S, K, T, r, sigma):
    # S and T are likely 2D arrays from np.meshgrid
    # We use np.maximum(T, 1e-9) to avoid dividing by zero at expiration
    T = np.maximum(T, 1e-9)
    
    # 1. Calculate d1 and d2
    d1 = calculate_d1_term(S, K, T, r, sigma)
    d2 = calculate_d2_term(d1, sigma, T)
    
    # 2. Price (Call)
    price = calculate_black_scholes(S, K, T, r, sigma)
    
    # 3. Delta (Price Sensitivity)
    delta = calculate_delta(S, K, T, r, sigma)
    
    # 4. Gamma (Sensitivity of Delta)
    gamma = calculate_gamma(S, K, T, r, sigma)
    
    # 5. Vega (Volatility Sensitivity - divided by 100 for 1% move)
    vega = calculate_vega(S, K, T, r, sigma) / 100
    
    # 6. Theta (Time Decay - divided by 365 for daily decay)
    theta = calculate_theta(S, K, T, r, sigma) / 365
    
    return price, delta, gamma, vega, theta