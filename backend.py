"""FastAPI backend for Personal Assistant."""

from __future__ import annotations

from datetime import datetime
from typing import TypedDict

import yfinance as yf
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Personal Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


class StockData(TypedDict):
    ticker: str
    name: str
    price: float
    pct_change: float
    rank: int | None


def fetch_perf(tickers: list[str], period: str) -> dict[str, tuple[float, float]]:
    """Return ticker -> (price, pct_change)."""
    try:
        data = yf.download(
            tickers,
            period=period,
            interval="1d",
            progress=False,
            auto_adjust=False,
            group_by="ticker",
            threads=True,
        )
    except Exception:
        return {}

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
        except (KeyError, ValueError, IndexError, AttributeError):
            continue
    return results


@app.get("/api/watchlist")
def get_watchlist(period: str = "6d") -> dict[str, list[StockData]]:
    """Get watchlist data."""
    perf = fetch_perf(list(WATCHLIST.values()), period)
    stocks: list[StockData] = []
    for name, ticker in WATCHLIST.items():
        if ticker in perf:
            price, pct = perf[ticker]
            stocks.append({
                "ticker": ticker,
                "name": name,
                "price": price,
                "pct_change": pct,
                "rank": None,
            })
    if not stocks:
        raise HTTPException(status_code=503, detail="Data unavailable")
    return {"data": stocks, "timestamp": datetime.now().isoformat()}


@app.get("/api/top-movers")
def get_top_movers(
    region: str = "us",
    period: str = "6d",
    limit: int = 5,
) -> dict[str, list[StockData]]:
    """Get top movers by region."""
    universe = US_UNIVERSE if region == "us" else SG_UNIVERSE
    perf = fetch_perf(universe, period)
    ranked = sorted(perf.items(), key=lambda kv: kv[1][1], reverse=True)[:limit]
    stocks: list[StockData] = [
        {
            "ticker": t,
            "name": t,
            "price": price,
            "pct_change": pct,
            "rank": i + 1,
        }
        for i, (t, (price, pct)) in enumerate(ranked)
    ]
    if not stocks:
        raise HTTPException(status_code=503, detail="Data unavailable")
    return {"data": stocks, "region": region, "timestamp": datetime.now().isoformat()}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
