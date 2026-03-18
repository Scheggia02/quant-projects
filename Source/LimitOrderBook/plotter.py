import seaborn as sns
import matplotlib.pyplot as plt

def plot_lob_heatmap(heatmap_matrix, mid_price_history):

    # 3. Create the Plot
    plt.figure(figsize=(15, 8))
    
    # We use 'magma' or 'hot' colormaps because they look like professional terminals
    sns.heatmap(heatmap_matrix, cmap='magma', cbar_kws={'label': 'Order Volume'})
    
    # 4. Overlay the Price Line
    # We have to align the mid_price values to the heatmap's Y-axis grid
    plt.plot(mid_price_history, color='cyan', linewidth=2, label='Mid-Price (Fair Value)', alpha=0.8)

    plt.title("Project 4: LOB Liquidity Heatmap", fontsize=16)
    plt.xlabel("Time (Ticks)", fontsize=12)
    plt.ylabel("Price Level", fontsize=12)
    plt.legend()
    plt.show()