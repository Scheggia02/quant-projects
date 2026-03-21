from MathLibrary import math_library as ml
import pandas as pd
import sys
import json

class MarketPoint:
    def __init__(self, date, price, volume):
        self.date = date
        self.price = price
        self.volume = volume

class MarketData:
    def __init__(self, symbol, market_points):
        self.symbol = symbol
        self.market_points = market_points

    def get_start_date(self):
        return self.market_points[0].date
    
    def get_end_date(self):
        return self.market_points[-1].date

def read_market_data(file_path):
    # Json structure: {"symbol": "AAPL", "market_points": [{"date": "2022-01-01", "price": 150.0, "volume": 1000000}, ...]}
    market_points = []
    with open(file_path, 'r') as f:
        data = json.load(f)
        symbol = data["symbolName"]
        for point in data["marketPoints"]:
            market_points.append(MarketPoint(point["time"], point["price"], 0.0))
    
    return MarketData(symbol, market_points)
   

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

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: python strategy_analyzer.py <path_to_market_data_file>")
        sys.exit(1)

    market_data_file = args[0]
    market_data = read_market_data(market_data_file)
    print(f"Market Data for {market_data.symbol}:")

    analyze_strategy(market_data)    

if __name__ == "__main__":
    main()