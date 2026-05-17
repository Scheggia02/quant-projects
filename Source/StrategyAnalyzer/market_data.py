import pandas as pd

class MarketTick:
    def __init__(self, time, bid, ask, volume=0.0):
        self.time = time
        self.bid = bid
        self.ask = ask
        self.volume = volume

    @property
    def mid(self):
        return self.calculate_mid(self.bid, self.ask)

    @property
    def price(self):
        return self.mid

    @staticmethod
    def calculate_mid(bid, ask):
        if bid is not None and ask is not None:
            return (bid + ask) / 2

        return None

class OhlcBar:
    def __init__(self, start_time, open, high, low, close, volume=0.0):
        self.start_time = start_time
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

class MarketData:
    def __init__(self, ticks, symbolName, timeframe=None, barDuration=None):
        self.ticks = ticks or []
        self.symbol = symbolName
        self.timeframe = timeframe
        self.barDuration = barDuration

    def get_start_date(self):
        return self.ticks[0].time
    
    def get_end_date(self):
        return self.ticks[-1].time

    def to_bars(self, interval=None, price_field="price"):
        interval = self.normalize_interval(interval or self.barDuration or self.timeframe)
        if interval is None:
            raise ValueError("An interval is required, for example '1min', '5min', or '1h'.")

        if len(self.ticks) == 0:
            return []

        records = []
        for tick in self.ticks:
            price = getattr(tick, price_field)
            if price is None:
                continue

            records.append({
                "time": tick.time,
                "price": price,
                "volume": tick.volume or 0.0,
            })

        if len(records) == 0:
            return []

        frame = pd.DataFrame(records)
        frame["time"] = pd.to_datetime(frame["time"])
        frame = frame.set_index("time").sort_index()

        ohlc = frame["price"].resample(interval).ohlc()
        volume = frame["volume"].resample(interval).sum()

        bars = []
        for start_time, row in ohlc.dropna().iterrows():
            bars.append(OhlcBar(
                start_time=start_time,
                open=row["open"],
                high=row["high"],
                low=row["low"],
                close=row["close"],
                volume=volume.loc[start_time],
            ))

        return bars

    @staticmethod
    def normalize_interval(interval):
        if interval is None:
            return None

        if not isinstance(interval, str):
            return interval

        timeframe_intervals = {
            "tick": None,
            "minute": "1min",
            "hour": "1h",
            "daily": "1D",
            "day": "1D",
            "weekly": "1W",
            "week": "1W",
        }
        normalized_interval = timeframe_intervals.get(interval.lower())
        if normalized_interval is not None:
            return normalized_interval

        if ":" in interval:
            return pd.Timedelta(interval)

        return interval
