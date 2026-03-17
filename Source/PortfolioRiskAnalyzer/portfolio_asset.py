import yfinance as yf

class PortfolioAsset:
    def __init__(self, name, weight, start_date, end_date):
        self.name = name
        self.weight = weight
        self.start_date = start_date
        self.end_date = end_date
        data = yf.download(self.name, start=self.start_date, end=self.end_date, progress=False)["Close"].squeeze()
        returns = data.pct_change().dropna().rename("return")
        returns.index.name = "date"
        self.returns = returns.reset_index()
