from statsmodels.tsa.stattools import coint
from statsmodels.regression.linear_model import OLS

import statsmodels.api as sm
import numpy as np
import pandas as pd

# Check if two assets are cointegrated and return the p-value
def check_cointegration(asset1, asset2, start_date, end_date):
    score, p_value, _ = coint(asset1.prices, asset2.prices)
    return p_value

# Scan a list of assets for cointegration and return pairs with p-value < 0.05
def scan_for_cointegration(assets, start_date, end_date, threshold=0.05):
    pairs = []
    for i in range(len(assets)):
        for j in range(i + 1, len(assets)):
            p_value = check_cointegration(assets[i], assets[j], start_date, end_date)
            if p_value < threshold:  # Threshold for cointegration
                pairs.append((assets[i], assets[j], p_value))
    return pairs

def calculate_beta(asset1_prices, asset2_prices):
    # Prepare indipendent variable (asset2) and dependent variable (asset1)
    X = asset2_prices.values

    X = sm.add_constant(X)  # Add intercept to the model, making it a linear regression
    y = asset1_prices.values

    # Fit the OLS regression model
    model = OLS(y, X).fit()
    
    # params[0] = Intercept (Alpha)
    # params[1] = Hedge Ratio (Beta)
    return model.params[1]  # Return the beta (hedge ratio)

def calculate_spread(asset1_prices, asset2_prices, beta):
    # Calculate the spread using the formula: Spread = Asset1 - Beta * Asset2
    spread = asset1_prices - beta * asset2_prices
    return spread

def calculate_zscore(spread):
    # Calculate the z-score of the spread
    mean = spread.mean()
    std = spread.std()
    zscore = (spread - mean) / std
    return zscore

def calculate_rolling_zscore(spread, window=20):
    # Calculate the rolling mean and standard deviation of the spread
    rolling_mean = spread.rolling(window=window).mean()
    rolling_std = spread.rolling(window=window).std()
    
    # Calculate the rolling z-score
    rolling_zscore = (spread - rolling_mean) / rolling_std
    return rolling_zscore

def generate_trading_signals(zscore, entry_threshold=2.0, exit_threshold=0.5):
    signals = []
    for z in zscore:
        if z > entry_threshold:
            signals.append(-1)  # Short signal
        elif z < -entry_threshold:
            signals.append(1)   # Long signal
        elif abs(z) < exit_threshold:
            signals.append(0)   # Exit signal
        else:
            signals.append(np.nan)  # No action
    return signals

def backtest_strategy(asset1_prices, asset2_prices, beta, entry_threshold=2.0, exit_threshold=0.5):
    # Ensure we are using the same dates for everything
    idx = asset1_prices.index 
    
    # 1. Calculate the PRICE Spread (The Rubber Band)
    price_spread = asset1_prices - (beta * asset2_prices)
    
    # 2. Calculate Z-Score (Use the function we built earlier)
    z_score = calculate_zscore(price_spread)
    
    # 3. Generate Signals and FORWARD FILL them
    raw_signals = generate_trading_signals(z_score, entry_threshold, exit_threshold)
    
    # CRITICAL: We MUST attach the index 'idx' here to stay in the 2020s!
    position = pd.Series(raw_signals, index=idx).ffill().fillna(0)
    
    # 4. Calculate Daily Returns
    asset1_ret = asset1_prices.pct_change().fillna(0)
    asset2_ret = asset2_prices.pct_change().fillna(0)
    
    # 5. Strategy Math
    spread_return = asset1_ret - (beta * asset2_ret)
    
    # Shift position by 1 (Trade on yesterday's signal for today's price)
    strategy_returns = position.shift(1).fillna(0) * spread_return
    
    # 6. Cumulative Growth (The Equity Curve)
    # We use .fillna(0) inside the cumprod to prevent vertical lines
    equity_curve = (1 + strategy_returns).cumprod()
    
    return equity_curve, z_score, strategy_returns

def calculate_backtest_metrics(equity_curve, strategy_returns, trading_days=252):
    total_return = equity_curve.iloc[-1] - 1
    
    sharpe_ratio = (strategy_returns.mean() / strategy_returns.std()) * np.sqrt(trading_days) if strategy_returns.std() != 0 else 0

    drawdown = equity_curve / equity_curve.cummax() - 1
    max_drawdown = drawdown.min()

    return total_return, sharpe_ratio, max_drawdown