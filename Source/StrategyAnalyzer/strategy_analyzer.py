from MathLibrary import math_library as ml
import pandas as pd
   
def analyze_strategy(market_data):
    print(f"Analyzing strategy for {market_data.symbol}...")

    data_prices = pd.Series([point.price for point in market_data.market_points], index=pd.to_datetime([point.date for point in market_data.market_points]))
    N = 100
    data_prices = data_prices.head(N)

    log_returns = ml.calculate_log_returns(data_prices)
    mean_return = ml.calculate_mean(log_returns)
    volatility = ml.calculate_volatility(log_returns)
    skewness = ml.calculate_skewness(log_returns)
    kurtosis = ml.calculate_kurtosis(log_returns)

    print(f"Mean Return: {mean_return:.4f}")
    print(f"Volatility: {volatility:.4f}")
    print(f"Skewness: {skewness:.4f}")
    print(f"Kurtosis: {kurtosis:.4f}")