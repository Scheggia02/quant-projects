#import sys
from StrategyAnalyzer.market_data import *
from strategy_analyzer import *
import json

def read_market_data(file_path):
    # Json structure: {"symbol": "AAPL", "market_points": [{"date": "2022-01-01", "price": 150.0, "volume": 1000000}, ...]}
    market_points = []
    with open(file_path, 'r') as f:
        data = json.load(f)
        symbol = data["symbolName"]
        for point in data["marketPoints"]:
            market_points.append(MarketPoint(point["time"], point["price"], 0.0))
    
    return MarketData(symbol, market_points)

def main():
    print("Running Strategy Analyzer...")
    
    # args = sys.argv[1:]
    # if len(args) != 1:
    #     print("Usage: python strategy_analyzer.py <path_to_market_data_file>")
    #     sys.exit(1)
    #     return

    market_data_file = "C:\\Users\\Dom\\Documents\\cAlgo\\Data\\cBots\\GhostMachine\\Data\\MarketData.json"  #args[0]
    market_data = read_market_data(market_data_file)
    print(f"Market Data for {market_data.symbol}:")

    analyze_strategy(market_data)

if __name__ == "__main__":
    main()