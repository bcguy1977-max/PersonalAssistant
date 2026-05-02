#!/usr/bin/env python3
"""Personal Assistant: market snapshot for a watchlist plus top movers."""

from datetime import datetime

import yfinance as yf
from rich.console import Console
from rich.table import Table

WATCHLIST = {
    "NVIDIA": "NVDA",
    "Apple": "AAPL",
    "VOO (S&P 500 ETF)": "VOO",
    "DBS Bank": "D05.SI",
}

US_UNIVERSE = [
    "NVDA", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "BRK-B",
    "AVGO", "JPM", "V", "WMT", "MA", "JNJ", "XOM", "UNH", "PG", "HD",
    "COST", "ORCL", "BAC", "ADBE", "NFLX", "CRM", "AMD", "KO", "PEP",
    "TMO", "CVX", "ABBV", "LLY", "MRK", "ACN", "MCD", "DIS", "INTC",
    "QCOM", "TXN", "IBM", "GE",
]

SG_UNIVERSE = [
    "D05.SI", "O39.SI", "U11.SI", "Z74.SI", "9CI.SI", "S63.SI",
    "BN4.SI", "S68.SI", "F34.SI", "J36.SI", "C38U.SI",
    "A17U.SI", "ME8U.SI", "C09.SI", "G13.SI", "H78.SI", "Y92.SI",
    "U96.SI", "BS6.SI", "N2IU.SI", "M44U.SI", "AJBU.SI", "C07.SI",
]


def fetch_perf(tickers, period="6d"):
    """Return ticker -> (last_price, pct_change_over_period)."""
    data = yf.download(
        tickers,
        period=period,
        interval="1d",
        progress=False,
        auto_adjust=False,
        group_by="ticker",
        threads=True,
    )
    results = {}
    for t in tickers:
        try:
            closes = data["Close"] if len(tickers) == 1 else data[t]["Close"]
            closes = closes.dropna()
            if len(closes) < 2:
                continue
            price = float(closes.iloc[-1])
            start = float(closes.iloc[0])
            pct = (price - start) / start * 100
            results[t] = (price, pct)
        except (KeyError, ValueError, IndexError):
            continue
    return results


def fmt_pct(pct):
    color = "green" if pct >= 0 else "red"
    return f"[{color}]{pct:+.2f}%[/{color}]"


def render_watchlist(console):
    perf = fetch_perf(list(WATCHLIST.values()))
    table = Table(title="Watchlist — last ~5 trading days")
    table.add_column("Name")
    table.add_column("Ticker")
    table.add_column("Price", justify="right")
    table.add_column("5d %", justify="right")
    for name, ticker in WATCHLIST.items():
        if ticker not in perf:
            table.add_row(name, ticker, "n/a", "n/a")
            continue
        price, pct = perf[ticker]
        table.add_row(name, ticker, f"{price:,.2f}", fmt_pct(pct))
    console.print(table)


def render_top(console, title, universe):
    perf = fetch_perf(universe)
    ranked = sorted(perf.items(), key=lambda kv: kv[1][1], reverse=True)[:5]
    table = Table(title=title)
    table.add_column("Rank", justify="right")
    table.add_column("Ticker")
    table.add_column("Price", justify="right")
    table.add_column("5d %", justify="right")
    for i, (ticker, (price, pct)) in enumerate(ranked, 1):
        table.add_row(str(i), ticker, f"{price:,.2f}", fmt_pct(pct))
    console.print(table)


def main():
    console = Console()
    console.print(
        f"[bold]Personal Assistant — Market Snapshot[/bold] "
        f"({datetime.now():%Y-%m-%d %H:%M})\n"
    )
    render_watchlist(console)
    console.print()
    render_top(console, "Top 5 US movers (5d, large-cap universe)", US_UNIVERSE)
    console.print()
    render_top(console, "Top 5 Singapore movers (5d, STI + REITs)", SG_UNIVERSE)


if __name__ == "__main__":
    main()
