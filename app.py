"""Personal Assistant — Streamlit web app for market snapshots."""

from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st
import yfinance as yf

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

PERIOD_MAP = {
    "1 day": ("2d", "1d %"),
    "5 days": ("6d", "5d %"),
    "1 month": ("1mo", "1mo %"),
    "3 months": ("3mo", "3mo %"),
    "1 year": ("1y", "1y %"),
}


@st.cache_data(ttl=300)
def fetch_perf(tickers: tuple[str, ...], period: str) -> dict[str, tuple[float, float]]:
    """Return ticker -> (last_price, pct_change_over_period). Cached 5 min."""
    data = yf.download(
        list(tickers),
        period=period,
        interval="1d",
        progress=False,
        auto_adjust=False,
        group_by="ticker",
        threads=True,
    )
    results: dict[str, tuple[float, float]] = {}
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


def style_pct(v: float) -> str:
    color = "#16a34a" if v >= 0 else "#dc2626"
    return f"color: {color}; font-weight: 600"


def watchlist_df(period: str) -> pd.DataFrame:
    perf = fetch_perf(tuple(WATCHLIST.values()), period)
    rows = []
    for name, ticker in WATCHLIST.items():
        price, pct = perf.get(ticker, (None, None))
        rows.append({"Name": name, "Ticker": ticker, "Price": price, "% change": pct})
    return pd.DataFrame(rows)


def top_movers_df(universe: list[str], period: str, n: int = 5) -> pd.DataFrame:
    perf = fetch_perf(tuple(universe), period)
    ranked = sorted(perf.items(), key=lambda kv: kv[1][1], reverse=True)[:n]
    return pd.DataFrame(
        [{"Ticker": t, "Price": p, "% change": pct} for t, (p, pct) in ranked]
    )


def render_table(df: pd.DataFrame) -> None:
    styled = (
        df.style.format({"Price": "{:,.2f}", "% change": "{:+.2f}%"}, na_rep="n/a")
        .map(lambda v: style_pct(v) if isinstance(v, (int, float)) else "", subset=["% change"])
    )
    st.dataframe(styled, hide_index=True, use_container_width=True)


def main() -> None:
    st.set_page_config(page_title="Personal Assistant", page_icon="📈", layout="wide")
    st.title("📈 Personal Assistant")
    st.caption(f"Market snapshot — {datetime.now():%Y-%m-%d %H:%M}")

    label = st.sidebar.selectbox("Lookback window", list(PERIOD_MAP.keys()), index=1)
    period, _pct_col = PERIOD_MAP[label]
    if st.sidebar.button("Refresh now"):
        st.cache_data.clear()
        st.rerun()
    st.sidebar.caption("Data: Yahoo Finance · cached 5 min")

    st.subheader("Watchlist")
    render_table(watchlist_df(period))

    col_us, col_sg = st.columns(2)
    with col_us:
        st.subheader(f"Top 5 US movers ({label})")
        render_table(top_movers_df(US_UNIVERSE, period))
    with col_sg:
        st.subheader(f"Top 5 Singapore movers ({label})")
        render_table(top_movers_df(SG_UNIVERSE, period))


if __name__ == "__main__":
    main()
