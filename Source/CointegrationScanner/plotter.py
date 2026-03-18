import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scanner import *

def plot_cointegration_heatmap(assets, start, end):
    n = len(assets)
    # Initialize an empty matrix
    pvalue_matrix = np.ones((n, n)) 
    
    for i in range(n):
        for j in range(i + 1, n):
            # Use your existing check_cointegration logic
            p_value = check_cointegration(assets[i], assets[j], start, end)
            pvalue_matrix[i, j] = p_value
            pvalue_matrix[j, i] = p_value # Symmetry
            
    # Plotting
    plt.figure(figsize=(10, 8))
    sns.heatmap(pvalue_matrix, xticklabels=assets, yticklabels=assets, 
                cmap='RdYlGn_r', annot=True)
    plt.title("Cointegration P-Values (Green = Tradable Pair)")
    plt.show()

    import matplotlib.pyplot as plt

def plot_backtest_results(equity_curve, z_score):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

    # Top Plot: The Money (Equity Curve)
    ax1.plot(equity_curve, label='Pairs Strategy', color='green', linewidth=2)
    ax1.axhline(1, color='black', linestyle='--', alpha=0.5) # The "Break Even" line
    ax1.set_title("Strategy Cumulative Returns (Growth of $1)")
    ax1.legend()

    # Bottom Plot: The Z-Score (The 'Heartbeat' that triggered the trades)
    ax2.plot(z_score, label='Z-Score', color='blue', alpha=0.7)
    ax2.axhline(2, color='red', linestyle='--')  # Sell Threshold
    ax2.axhline(-2, color='red', linestyle='--') # Buy Threshold
    ax2.axhline(0, color='black', alpha=0.3)     # The Mean
    ax2.set_title("Z-Score Signals (Entry/Exit Points)")
    
    plt.tight_layout()
    plt.show()

def plot_strategy_metrics(strategy_returns, equity_curve, total_return, sharpe_ratio, max_drawdown):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

    # Top Plot: The Money (Equity Curve)
    ax1.plot(equity_curve, label='Pairs Strategy', color='green', linewidth=2)
    ax1.axhline(1, color='black', linestyle='--', alpha=0.5) # The "Break Even" line
    ax1.set_title(f"Strategy Cumulative Returns (Growth of $1)\nTotal Return: {total_return:.2%}, Sharpe Ratio: {sharpe_ratio:.2f}, Max Drawdown: {max_drawdown:.2%}")
    ax1.legend()

    # Bottom Plot: Daily Strategy Returns
    ax2.plot(strategy_returns, label='Daily Strategy Returns', color='blue', alpha=0.7)
    ax2.axhline(0, color='black', alpha=0.3)     # The Zero Line
    ax2.set_title("Daily Strategy Returns")
    
    plt.tight_layout()
    plt.show()