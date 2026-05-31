import unittest
from unittest.mock import patch

import matplotlib.pyplot as plt

from StrategyAnalyzer.market_data import MarketData, MarketTick, OhlcBar


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

    def test_to_ohlc_frame_converts_all_bars_for_mplfinance(self):
        bars = [
            OhlcBar("2024-01-01 00:00:00", 100.0, 101.0, 99.0, 100.5, 10),
            OhlcBar("2024-01-01 01:00:00", 100.5, 102.0, 100.0, 101.5, 11),
            OhlcBar("2024-01-01 02:00:00", 101.5, 103.0, 101.0, 102.5, 12),
        ]

        frame = MarketData.to_ohlc_frame(bars)

        self.assertEqual(len(frame), len(bars))
        self.assertEqual(list(frame.columns), ["Open", "High", "Low", "Close", "Volume"])
        self.assertEqual(frame.iloc[0].to_dict(), {
            "Open": 100.0,
            "High": 101.0,
            "Low": 99.0,
            "Close": 100.5,
            "Volume": 10,
        })

    def test_plot_bars_uses_mplfinance(self):
        bars = [
            OhlcBar("2024-01-01 00:00:00", 100.0, 101.0, 99.0, 100.5, 10),
            OhlcBar("2024-01-01 01:00:00", 100.5, 102.0, 100.0, 101.5, 11),
        ]
        figure, axes = plt.subplots()

        with patch("StrategyAnalyzer.market_data.mpf.plot", return_value=(figure, [axes])) as plot:
            result_figure, result_axes = MarketData.plot_bars(
                bars,
                symbol="TEST",
                interval="1h",
                width_scale=2.0,
                price_padding=0.1,
                figsize=(14, 6),
                show=False,
                show_close_line=False,
            )

        try:
            plotted_frame = plot.call_args.args[0]
            plot_options = plot.call_args.kwargs

            self.assertEqual(len(plotted_frame), len(bars))
            self.assertEqual(plot_options["type"], "candle")
            self.assertEqual(plot_options["style"], "charles")
            self.assertEqual(plot_options["title"], "TEST - 1h OHLC Chart")
            self.assertEqual(plot_options["scale_width_adjustment"], {"candle": 2.0})
            self.assertEqual(plot_options["ylim"], (98.7, 102.3))
            self.assertEqual(plot_options["figsize"], (14, 6))
            self.assertIs(result_figure, figure)
            self.assertIs(result_axes, axes)
        finally:
            plt.close(figure)

    def test_plot_bar_chart_uses_to_bars_once(self):
        market_data = MarketData(ticks=[], symbolName="TEST")
        bars = [OhlcBar("2024-01-01 00:00:00", 100.0, 101.0, 99.0, 100.5, 10)]

        with patch.object(market_data, "to_bars", return_value=bars) as to_bars:
            with patch("StrategyAnalyzer.market_data.MarketData.plot_bars") as plot_bars:
                market_data.plot_bar_chart("1h", "bid")

        to_bars.assert_called_once_with(interval="1h", price_field="bid")
        plot_bars.assert_called_once_with(bars, symbol="TEST", interval="1h")

    def test_plot_bar_chart_forwards_plot_options(self):
        market_data = MarketData(ticks=[], symbolName="TEST")
        bars = [OhlcBar("2024-01-01 00:00:00", 100.0, 101.0, 99.0, 100.5, 10)]

        with patch.object(market_data, "to_bars", return_value=bars):
            with patch("StrategyAnalyzer.market_data.MarketData.plot_bars") as plot_bars:
                market_data.plot_bar_chart("1h", "bid", width_scale=2.0, price_padding=0.02)

        plot_bars.assert_called_once_with(
            bars,
            symbol="TEST",
            interval="1h",
            width_scale=2.0,
            price_padding=0.02,
        )

    def test_calculate_price_limits_uses_price_padding(self):
        bars = [
            OhlcBar("2024-01-01 00:00:00", 100.0, 101.0, 99.0, 100.5, 10),
            OhlcBar("2024-01-01 01:00:00", 100.5, 102.0, 100.0, 101.5, 11),
        ]
        frame = MarketData.to_ohlc_frame(bars)

        self.assertEqual(MarketData.calculate_price_limits(frame, 0.1), (98.7, 102.3))

    def test_plot_bars_can_add_close_line(self):
        bars = [
            OhlcBar("2024-01-01 00:00:00", 100.0, 100.0, 100.0, 100.0, 10),
            OhlcBar("2024-01-01 01:00:00", 101.0, 101.0, 101.0, 101.0, 11),
        ]
        figure, axes = plt.subplots()

        with patch("StrategyAnalyzer.market_data.mpf.make_addplot", return_value="close-line") as make_addplot:
            with patch("StrategyAnalyzer.market_data.mpf.plot", return_value=(figure, [axes])) as plot:
                MarketData.plot_bars(bars, symbol="TEST", interval="1h", show=False)

        try:
            make_addplot.assert_called_once()
            self.assertEqual(plot.call_args.kwargs["addplot"], "close-line")
        finally:
            plt.close(figure)

    def test_plot_bars_handles_empty_bars(self):
        with patch("builtins.print") as print_function:
            result = MarketData.plot_bars([], show=False)

        self.assertIsNone(result)
        print_function.assert_called_once_with("No bars to plot.")


if __name__ == "__main__":
    unittest.main()