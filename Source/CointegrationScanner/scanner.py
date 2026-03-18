import yfinance as yf
from statsmodels.tsa.stattools import coint

# Check if two assets are cointegrated and return the p-value
def check_cointegration(asset1, asset2, start_date, end_date):
    data = yf.download([asset1, asset2], start_date, end_date, progress=False)["Close"].dropna()

    score, p_value, _ = coint(data[asset1], data[asset2])
    return p_value

# Scan a list of assets for cointegration and return pairs with p-value < 0.05
def scan_for_cointegration(assets, start_date, end_date, threshold=0.05):
    pairs = []
    for i in range(len(assets)):
        for j in range(i + 1, len(assets)):
            p_value = check_cointegration(assets[i], assets[j], start_date, end_date)
            if p_value < threshold:  # Threshold for cointegration
                pairs.append((assets[i], assets[j], p_value))
    return pairs