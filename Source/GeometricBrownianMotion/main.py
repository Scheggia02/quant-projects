from geometric_brownian_motion import *
import matplotlib.pyplot as plt

def main():
    print("Geometric Brownian Motion simulation.")

    # Simulation Params
    S0 = 100    # Starting Price
    r = 0.05    # 5% Risk-Free Rate
    sigma = 0.2 # 20% Volatility
    lambd = 1 # Risk Premium (Sharpe Ratio)
    T = 1.0     # 1 Year
    dt = 1/252  # Daily steps
    simulations = 100  # Number of paths to simulate

    calculate_gbm(S=S0, T=T, r=r, sigma=sigma, lambd=lambd, dt=dt, simulations=simulations).plot(
        title="Geometric Brownian Motion Simulation", ylabel="Price", xlabel="Time Steps", legend=False, figsize=(12, 6)
    )

    #calculate_gbm_wealth_index(T=T, r=r, sigma=sigma, lambd=lambd, dt=dt, simulations=simulations).plot(
    #    title="Geometric Brownian Motion Wealth Index", ylabel="Wealth Index", xlabel="Time Steps", legend=False, figsize=(12, 6)
    #)

    plt.show()

if __name__ == "__main__":
    main()