import unittest

from StrategyAnalyzer.market_data import MarketData, MarketTick, MarketTick


class TestMarketData(unittest.TestCase):
    def test_market_tick_calculates_mid_from_bid_and_ask(self):
        tick = MarketTick("2024-01-01 00:00:00", bid=1.1000, ask=1.1002, volume=10)

        self.assertAlmostEqual(tick.mid, 1.1001)
        self.assertAlmostEqual(tick.price, 1.1001)

    def test_to_bars_resamples_ticks_to_ohlcv(self):
        ticks = [
            MarketTick("2024-01-01 00:00:00", 100.0, 100.0, 1),
            MarketTick("2024-01-01 00:00:10", 101.0, 101.0, 2),
            MarketTick("2024-01-01 00:00:20", 99.0, 99.0, 3),
            MarketTick("2024-01-01 00:01:00", 102.0, 102.0, 4),
            MarketTick("2024-01-01 00:01:10", 103.0, 103.0, 5),
        ]
        market_data = MarketData(ticks=ticks, symbolName="TEST")
        bars = market_data.to_bars("1min")

        self.assertEqual(len(bars), 2)
        self.assertEqual(bars[0].open, 100.0)
        self.assertEqual(bars[0].high, 101.0)
        self.assertEqual(bars[0].low, 99.0)
        self.assertEqual(bars[0].close, 99.0)
        self.assertEqual(bars[0].volume, 6)
        self.assertEqual(bars[1].open, 102.0)
        self.assertEqual(bars[1].high, 103.0)
        self.assertEqual(bars[1].low, 102.0)
        self.assertEqual(bars[1].close, 103.0)
        self.assertEqual(bars[1].volume, 9)

    def test_to_bars_uses_bar_duration_when_interval_is_not_provided(self):
        ticks = [
            MarketTick("2024-01-01 00:00:00", 100.0, 100.0, 1),
            MarketTick("2024-01-01 00:30:00", 101.0, 101.0, 2),
            MarketTick("2024-01-01 01:00:00", 102.0, 102.0, 3),
        ]
        market_data = MarketData(ticks=ticks, symbolName="TEST", barDuration="01:00:00")
        bars = market_data.to_bars()

        self.assertEqual(len(bars), 2)
        self.assertEqual(bars[0].open, 100.0)
        self.assertEqual(bars[0].close, 101.0)
        self.assertEqual(bars[1].open, 102.0)


if __name__ == "__main__":
    unittest.main()