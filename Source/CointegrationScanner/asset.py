import yfinance as yf

class Asset:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        close_prices = yf.download(ticker, start=start_date, end=end_date, progress=False)["Close"].dropna()
        self.prices = close_prices.squeeze()