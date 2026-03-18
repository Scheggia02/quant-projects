from scanner import *
from plotter import *

def main():
    assets = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
    start_date = '2023-01-01'
    end_date = '2024-01-01'

    # Example: Testing "The Cola Wars"
    # pair_assets = scan_for_cointegration(assets, start_date, end_date)
    # for asset1, asset2, p_value in pair_assets:
    #     print(f"Cointegration P-Value between {asset1} and {asset2}: {p_value:.4f}") 

    plot_cointegration_heatmap(assets, start_date, end_date)

if __name__ == "__main__":
    main()