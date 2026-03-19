from limit_order_book import *
from plotter import *
import matplotlib.pyplot as plt

def main():
    # Generate the raw data
    lob_df, mid_price_history = simulate_limit_order_book(200)
    print("Sample of the Limit Order Book DataFrame:")
    print(lob_df.head())

    # Create a matrix where index=Price and columns=Time
    heatmap_data = lob_df.pivot_table(index='price', columns='timestamp', values='quantity').fillna(0)

    # Sort the price index so high prices are at the top
    heatmap_data = heatmap_data.sort_index(ascending=False)

    # 2. Define the 'Extent' (The Mapping Key)
    # [Left, Right, Bottom, Top]
    price_min, price_max = heatmap_data.index.min(), heatmap_data.index.max()

    obi = calculate_order_book_imbalance(lob_df)

    # Plot both charts in the same window
    fig = plt.figure(figsize=(16, 10))
    grid = fig.add_gridspec(
        2,
        2,
        height_ratios=[3, 1],
        width_ratios=[30, 1],
        hspace=0.15,
        wspace=0.08,
    )

    heatmap_ax = fig.add_subplot(grid[0, 0])
    imbalance_ax = fig.add_subplot(grid[1, 0], sharex=heatmap_ax)
    colorbar_ax = fig.add_subplot(grid[:, 1])

    plot_lob_heatmap(
        heatmap_data,
        mid_price_history,
        price_min,
        price_max,
        obi,
        heatmap_ax,
        colorbar_ax,
    )
    plot_ob_imbalance(obi, imbalance_ax)

    heatmap_ax.tick_params(axis='x', labelbottom=False)
    plt.show()

if __name__ == "__main__":
    main()