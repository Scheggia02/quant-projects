import numpy as np
import pandas as pd

class Order:
    def __init__(self, timestamp, price, quantity, side):
        self.timestamp = timestamp
        self.price = price
        self.quantity = quantity
        self.side = side  # 'bid' or 'ask'

    def get_dataframe(self):
        return pd.DataFrame({
            'timestamp': [self.timestamp],
            'price': [self.price],
            'quantity': [self.quantity],
            'side': [self.side]
        })

def simulate_limit_order_book(num_ticks=100, num_levels=50):
    mid_price = 100.0
    mid_price_history = []
    orders = []

    # Generate bids and asks, simulate higher volume near the mid price
    for t in range(num_ticks):
        # 1. Move the price ONCE per tick
        mid_price += np.random.normal(0, 0.1)
        mid_price_history.append(mid_price) # Append ONCE per tick

        # 2. Generate Bids AND Asks for this specific moment in time
        for level in range(1, num_levels + 1):
            # Bid Logic (Below Mid)
            bid_p = np.round(mid_price - level * 0.05, 2)
            bid_v = np.random.poisson(lam=20 * np.exp(-0.1 * level))
            orders.append({'timestamp': t, 'price': bid_p, 'quantity': bid_v, 'side': 'bid'})

            # Ask Logic (Above Mid)
            ask_p = np.round(mid_price + level * 0.05, 2)
            ask_v = np.random.poisson(lam=20 * np.exp(-0.1 * level))
            orders.append({'timestamp': t, 'price': ask_p, 'quantity': ask_v, 'side': 'ask'})

    # Create the DataFrame directly from the list of dicts (much faster than pd.concat)
    return pd.DataFrame(orders), mid_price_history