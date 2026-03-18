from option_library import *
from plotter import plot_3d_option_surface
import numpy as np

def run_option_calculations():
    spot_range = np.linspace(80, 120, 10)
    time_range = np.linspace(1, 30, 30)
    K = 100

    # Loop through spot prices and calculate option price and Greeks for each combination of spot price and time
    for i in range(len(spot_range)):
        S = spot_range[i]
        for j in range(len(time_range)):
            T = time_range[j] / 365  # Convert days to years
            r = 0.05
            sigma = 0.2 

            option_price = calculate_black_scholes(S, K, T, r, sigma)
            delta = calculate_delta(S, K, T, r, sigma)
            gamma = calculate_gamma(S, K, T, r, sigma)
            theta = calculate_theta(S, K, T, r, sigma)
            vega = calculate_vega(S, K, T, r, sigma)

            print(f"Spot Price: {S:.2f}, Option Price: {option_price:.2f}, Delta: {delta:.4f}, Gamma: {gamma:.6f}, Theta: {theta:.4f}, Vega: {vega:.4f}")

def generate_surface_data():
    K = 100
    r = 0.05
    sigma = 0.2

    # 1. Define the ranges
    spot_range = np.linspace(80, 120, 50)  # X-axis (Price)
    time_range = np.linspace(1, 30, 30) / 365  # Y-axis (Time in years)

    # 2. Create the coordinate system
    S, T = np.meshgrid(spot_range, time_range)

    # 3. Run the engine
    prices, deltas, gammas, vegas, thetas = calculate_bs_metrics(S, K, T, r, sigma)

    # 4. Plot the surfaces
    plot_3d_option_surface(S, T, prices, deltas, gammas)

if __name__ == "__main__":
    generate_surface_data()