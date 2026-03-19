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

    # 2. Define the 'Extent' (The Mapping Key)
    # [Left, Right, Bottom, Top]
    price_min, price_max = heatmap_data.index.min(), heatmap_data.index.max()
    time_min, time_max = 0, len(mid_price_history)

    # Plot the heatmap
    plot_lob_heatmap(heatmap_data, mid_price_history, time_min, time_max, price_min, price_max)

    # Plot the imbalance
    #obi = calculate_order_book_imbalance(lob_df)
    #plot_ob_imbalance(obi)

if __name__ == "__main__":
    main()