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
