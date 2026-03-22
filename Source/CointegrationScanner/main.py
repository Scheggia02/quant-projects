from scanner import *
from plotter import *
from asset import Asset

def main():
    start_date = '2023-01-01'
    end_date = '2024-01-01'
    asset_objects = [Asset(ticker, start_date, end_date) for ticker in ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']]

    pair_assets = scan_for_cointegration(asset_objects)
    for asset1, asset2, p_value in pair_assets:

        beta = calculate_beta(asset1.prices, asset2.prices)
        equity_curve, z_score, strategy_returns = backtest_strategy(asset1.prices, asset2.prices, beta)
        total_return, sharpe_ratio, max_drawdown = calculate_backtest_metrics(equity_curve, strategy_returns)
        
        print(f"Cointegrated Pair: {asset1.ticker} & {asset2.ticker} with p-value: {p_value:.4f} | Total Return: {total_return:.2%} | Sharpe Ratio: {sharpe_ratio:.2f} | Max Drawdown: {max_drawdown:.2%}")
        #plot_strategy_metrics(strategy_returns, equity_curve, total_return, sharpe_ratio, max_drawdown)

    plot_cointegration_heatmap(asset_objects)

if __name__ == "__main__":
    main()