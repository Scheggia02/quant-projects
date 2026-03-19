import seaborn as sns
import matplotlib.pyplot as plt

def plot_lob_heatmap(heatmap_data, mid_price_history, price_min, price_max, obi_series, ax=None, cax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 7))
    else:
        fig = ax.figure

    time_values = heatmap_data.columns.to_numpy()
    time_min = time_values[0] - 0.5
    time_max = time_values[-1] + 0.5

    # This represents the "Total Net Pressure" over time
    cumulative_obi = obi_series.cumsum()

    # 3. Use imshow with EXTENT
    # This tells Matplotlib: "This image covers prices from X to Y"
    im = ax.imshow(heatmap_data.values, aspect='auto', cmap='magma', 
                   interpolation='none', # Keeps the 'Poisson' blocks sharp
                   extent=[time_min, time_max, price_min, price_max])

    # 4. Now the line will 'HUG' the liquidity perfectly
    mid_price_line, = ax.plot(
        time_values,
        mid_price_history,
        color='cyan',
        linewidth=1.5,
        label='Mid Price',
        alpha=0.7,
    )
    ax.set_xlim(time_min, time_max)
    ax.legend(handles=[mid_price_line], loc='upper left', fontsize='small')

    ax_twin = ax.twinx()
    cumulative_obi_line, = ax_twin.plot(
        time_values,
        cumulative_obi,
        color='lime',
        linewidth=0.8,
        label='Cumulative OBI',
        alpha=0.7,
    )
    ax_twin.legend(handles=[cumulative_obi_line], loc='upper right', fontsize='small')
    ax_twin.set_yticks([])

    ax.set_title("Project 4: LOB Heatmap (Corrected Alignment)")
    ax.set_xlabel("Time (Ticks)")
    ax.set_ylabel("Price ($)")

    fig.colorbar(im, cax=cax, ax=ax, label='Order Volume')

def plot_ob_imbalance(obi_series, ax=None):
    if ax is None:
        _, ax = plt.subplots(figsize=(12, 4))

    ax.plot(obi_series.index, obi_series.values, color='blue', label='Order Book Imbalance')
    ax.axhline(0, color='gray', linestyle='--', linewidth=0.5)
    ax.set_xlim(obi_series.index.min() - 0.5, obi_series.index.max() + 0.5)
    ax.set_title("Order Book Imbalance Over Time")
    ax.set_xlabel("Time (Ticks)")
    ax.set_ylabel("Imbalance")
    ax.legend()