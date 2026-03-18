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