from dynamic_option_visualizer import DynamicOptionVisualizer
import numpy as np

def test_option_visualizer():
    spot_range = np.linspace(80, 120, 10)
    time_range = np.linspace(1, 30, 30) / 365  # Y-axis (Time in years)
    K = 100
    r = 0.05
    sigma = 0.2
    
    dynamic_visualizer = DynamicOptionVisualizer(spot_range, time_range, K, r, sigma)
    dynamic_visualizer.run_option_calculations()
    dynamic_visualizer.generate_surface_data()

if __name__ == "__main__":
    test_option_visualizer()