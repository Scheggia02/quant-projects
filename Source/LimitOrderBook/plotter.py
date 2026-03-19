import seaborn as sns
import matplotlib.pyplot as plt

def plot_lob_heatmap(heatmap_data, mid_price_history, time_min, time_max, price_min, price_max):
    plt.figure(figsize=(12, 7))

    # 3. Use imshow with EXTENT
    # This tells Matplotlib: "This image covers prices from X to Y"
    im = plt.imshow(heatmap_data.values, aspect='auto', cmap='magma', 
                    interpolation='none', # Keeps the 'Poisson' blocks sharp
                    extent=[time_min, time_max, price_min, price_max])

    # 4. Now the line will 'HUG' the liquidity perfectly
    plt.plot(mid_price_history, color='cyan', linewidth=1, label='Mid Price', alpha=0.7)

    plt.colorbar(im, label='Order Volume')
    plt.title("Project 4: LOB Heatmap (Corrected Alignment)")
    plt.xlabel("Time (Ticks)")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.show()

def plot_ob_imbalance(obi_series):
    plt.figure(figsize=(12, 4))
    plt.plot(obi_series.index, obi_series.values, color='blue', label='Order Book Imbalance')
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.5)
    plt.title("Order Book Imbalance Over Time")
    plt.xlabel("Time (Ticks)")
    plt.ylabel("Imbalance")
    plt.legend()
    plt.show()