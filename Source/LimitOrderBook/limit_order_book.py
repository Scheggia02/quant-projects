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

def simulate_limit_order_book(num_ticks=100, num_levels=50, alpha=0.5):
    mid_price = 100.0
    mid_price_history = []
    orders = []

    # Generate bids and asks, simulate higher volume near the mid price
    for t in range(num_ticks):
        # 1. Record the mid price for this tick
        mid_price_history.append(mid_price)

        # 2. Generate the LOB for this tick
        tick_bid_vol = 0
        tick_ask_vol = 0

        # 3. Generate Bids AND Asks for this specific moment in time
        for level in range(1, num_levels + 1):
            # Bid Logic (Below Mid)
            bid_p = np.round(mid_price - level * 0.05, 2)
            bid_v = np.random.poisson(lam=20 * np.exp(-0.1 * level))
            orders.append({'timestamp': t, 'price': bid_p, 'quantity': bid_v, 'side': 'bid'})
            tick_bid_vol += bid_v

            # Ask Logic (Above Mid)
            ask_p = np.round(mid_price + level * 0.05, 2)
            ask_v = np.random.poisson(lam=20 * np.exp(-0.1 * level))
            orders.append({'timestamp': t, 'price': ask_p, 'quantity': ask_v, 'side': 'ask'})
            tick_ask_vol += ask_v

        obi = (tick_bid_vol - tick_ask_vol) / (tick_bid_vol + tick_ask_vol)

        # 4. UPDATE THE PRICE for the NEXT tick based on OBI
        # Price = Old Price + Noise + (alpha * Imbalance)
        noise = np.random.normal(0, 0.05)
        mid_price += noise + alpha * obi

    # Create the DataFrame directly from the list of dicts (much faster than pd.concat)
    return pd.DataFrame(orders), mid_price_history


def calculate_order_book_imbalance(lob_df):
    volume_by_side = lob_df.groupby(['timestamp', 'side'])['quantity'].sum().unstack(fill_value=0)
    bid_volume = volume_by_side.get('bid', pd.Series(0, index=volume_by_side.index))
    ask_volume = volume_by_side.get('ask', pd.Series(0, index=volume_by_side.index))

    imbalance = (bid_volume - ask_volume) / (bid_volume + ask_volume)
    return imbalance