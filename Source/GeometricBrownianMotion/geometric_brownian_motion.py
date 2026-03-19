import numpy as np
import pandas as pd

def _get_time_grid(T, dt):
    if dt <= 0:
        raise ValueError("dt must be positive.")
    if T <= 0:
        raise ValueError("T must be positive.")

    steps = int(round(T / dt))
    if not np.isclose(steps * dt, T):
        raise ValueError("T must be an integer multiple of dt.")

    return steps, np.arange(steps + 1) * dt


def _simulate_gbm_growth_factors(T, r, sigma, lambd, dt, simulations):
    if simulations < 1:
        raise ValueError("simulations must be at least 1.")

    steps, t = _get_time_grid(T, dt)
    mu = r + (sigma * lambd)

    W = np.random.standard_normal(size=(steps, simulations))
    brownian_increments = W * np.sqrt(dt)
    brownian_paths = np.vstack([
        np.zeros((1, simulations)),
        np.cumsum(brownian_increments, axis=0),
    ])

    growth_factors = np.exp((mu - 0.5 * sigma**2) * t[:, None] + sigma * brownian_paths)
    return pd.DataFrame(growth_factors)

def calculate_gbm(S, T, r, sigma, lambd, dt, simulations=1):
    growth_factors = _simulate_gbm_growth_factors(T, r, sigma, lambd, dt, simulations)
    return S * growth_factors

def calculate_gbm_wealth_index(T, r, sigma, lambd, dt, simulations=1):
    return _simulate_gbm_growth_factors(T, r, sigma, lambd, dt, simulations)