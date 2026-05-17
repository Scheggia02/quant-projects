#import sys
from StrategyAnalyzer.market_data import *
from StrategyAnalyzer.strategy_analyzer import *
import json

def read_market_data(file_path):
    ticks = []
    with open(file_path, 'r') as f:
        data = json.load(f)
        symbol = data["symbolName"]
        timeframe = data["timeframeName"]
        barDuration = data["barDuration"]
        for tick in data["ticks"]:
            time = tick["time"]
            volume = tick.get("volume", 0.0)
            bid = tick.get("bid", tick.get("bidPrice"))
            ask = tick.get("ask", tick.get("askPrice"))

            if bid is not None and ask is not None:
                ticks.append(MarketTick(time, bid=bid, ask=ask, volume=volume))
            else:
                mid_price = MarketTick.calculate_mid(bid, ask)
                ticks.append(MarketTick(time, bid=mid_price, ask=mid_price, volume=volume))
    
    return MarketData(ticks=ticks, symbolName=symbol, timeframe=timeframe, barDuration=barDuration)

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