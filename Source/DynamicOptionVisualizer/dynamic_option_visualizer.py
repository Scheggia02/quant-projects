from option_library import *
from plotter import *
import numpy as np

class DynamicOptionVisualizer:
    def __init__(self, spot_range, time_range, K, r, sigma):
        self.spot_range = spot_range
        self.time_range = time_range
        self.K = K
        self.r = r
        self.sigma = sigma

    def run_option_calculations(self):
        K = self.K

        # Loop through spot prices and calculate option price and Greeks for each combination of spot price and time
        for i in range(len(self.spot_range)):
            S = self.spot_range[i]
            for j in range(len(self.time_range)):
                T = self.time_range[j]
                r = self.r
                sigma = self.sigma

                option_price = calculate_black_scholes(S, K, T, r, sigma)
                delta = calculate_delta(S, K, T, r, sigma)
                gamma = calculate_gamma(S, K, T, r, sigma)
                theta = calculate_theta(S, K, T, r, sigma)
                vega = calculate_vega(S, K, T, r, sigma)

                print(f"Spot Price: {S:.2f}, Option Price: {option_price:.2f}, Delta: {delta:.4f}, Gamma: {gamma:.6f}, Theta: {theta:.4f}, Vega: {vega:.4f}")

    def generate_surface_data(self):
        K = self.K
        r = self.r

        # 1. Generate the IV Grid
        iv_surface = calculate_volatility_surface(self.spot_range, K, self.sigma, skew=-0.15, smile=0.1)

        # 2. Create the coordinate system
        S, T = np.meshgrid(self.spot_range, self.time_range)

        # 3. Run the engine
        prices, deltas, gammas, vegas, thetas = calculate_bs_metrics(S, K, T, r, iv_surface)


        # 4. Plot the surfaces


        #create_pnl_simulator(S, T, prices)
        create_pnl_slider_demo(self.spot_range, K, r, self.sigma)
        #plot_3d_option_surface(S, T, prices, deltas, gammas)