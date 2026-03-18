from limit_order_book import *
from plotter import *

def main():
    # Generate the raw data
    lob_df, mid_price_history = simulate_limit_order_book(200)
    print(lob_df.head())

    # Create a matrix where index=Price and columns=Time
    heatmap_data = lob_df.pivot_table(index='price', columns='timestamp', values='quantity').fillna(0)

    # Sort the price index so high prices are at the top
    heatmap_data = heatmap_data.sort_index(ascending=False)

    # Plot the heatmap
    plot_lob_heatmap(heatmap_data, mid_price_history)

if __name__ == "__main__":
    main()