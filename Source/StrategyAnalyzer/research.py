import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import mplfinance as mpf

import StrategyAnalyzer.market_data as md


def plot_bar_chart(self, interval=None, price_field="price", **plot_options):
    bars = self.to_bars(interval=interval, price_field=price_field)
    return md.plot_bars(bars, symbol=self.symbol, interval=interval, **plot_options)


def plot_bar_close_series(
    bars_df, symbol, chart_width=1000, chart_height=400, price_padding=0.05
):
    y_min = bars_df["close"].min()
    y_max = bars_df["close"].max()
    y_pad = (y_max - y_min) * price_padding

    return (
        alt.Chart(bars_df)
        .mark_line()
        .encode(
            x="start_time:T",
            y=alt.Y(
                "close:Q",
                title="Close",
                scale=alt.Scale(domain=[y_min - y_pad, y_max + y_pad]),
            ),
        )
        .properties(
            title=f"{symbol} Close Price Over Time",
            width=chart_width,
            height=chart_height,
        )
    ).interactive()


def plot_bars(
    bars,
    symbol=None,
    interval=None,
    width_scale=1.0,
    price_padding=0.05,
    figsize=None,
    axes=None,
    show_close_line=True,
):
    bars = list(bars)
    if len(bars) == 0:
        print("No bars to plot.")
        return

    frame = md.MarketData.to_ohlc_frame(bars)
    interval_title = f"{interval} OHLC" if interval is not None else "OHLC"
    title = f"{symbol or 'Market Data'} - {interval_title} Chart"

    plot_options = {
        "type": "candle",
        "style": "charles",
        "title": title,
        "ylabel": "Price",
        "volume": False,
        "returnfig": axes is None,
        "scale_width_adjustment": {"candle": width_scale},
        "ylim": calculate_price_limits(frame, price_padding),
        "warn_too_much_data": len(frame) + 1,
    }
    if figsize is not None and axes is None:
        plot_options["figsize"] = figsize
    if show_close_line:
        addplot_options = {"color": "black", "width": 0.8}
        if axes is not None:
            addplot_options["ax"] = axes
        plot_options["addplot"] = mpf.make_addplot(frame["Close"], **addplot_options)

    if axes is None:
        figure, plot_axes = mpf.plot(frame, **plot_options)
        axes = plot_axes[0]
    else:
        plot_options["ax"] = axes
        mpf.plot(frame, **plot_options)
        figure = axes.figure

    plt.show()
    return figure, axes


def calculate_price_limits(frame, price_padding):
    if price_padding is None:
        return None

    low = frame["Low"].min()
    high = frame["High"].max()
    price_range = high - low
    if price_range == 0:
        price_range = max(abs(high), 1) * 0.01

    padding = price_range * price_padding
    return low - padding, high + padding
