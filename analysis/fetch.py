"""Fetch end-of-day market data via yfinance."""

import yfinance as yf
from datetime import date, timedelta


INDICES = {
    "SPY": "S&P 500",
    "QQQ": "Nasdaq 100",
    "DIA": "Dow Jones",
    "IWM": "Russell 2000",
    "^VIX": "VIX",
}

SECTORS = {
    "XLK": "Technology",
    "XLF": "Financials",
    "XLE": "Energy",
    "XLV": "Healthcare",
    "XLC": "Communication",
    "XLY": "Consumer Disc.",
    "XLP": "Consumer Staples",
    "XLI": "Industrials",
    "XLB": "Materials",
    "XLRE": "Real Estate",
    "XLU": "Utilities",
}

TOP_TICKERS = ["AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "TSLA", "NFLX"]


def _pct_change(ticker: str) -> dict:
    # end must be tomorrow for yfinance to include today's close
    end = date.today() + timedelta(days=1)
    start = end - timedelta(days=7)
    hist = yf.Ticker(ticker).history(start=start, end=end)
    if len(hist) < 2:
        return {"ticker": ticker, "close": None, "change_pct": None}
    close = hist["Close"].iloc[-1]
    prev = hist["Close"].iloc[-2]
    return {
        "ticker": ticker,
        "close": round(close, 2),
        "change_pct": round((close - prev) / prev * 100, 2),
    }


def fetch_market_data() -> dict:
    return {
        "date": date.today().isoformat(),
        "indices": {name: _pct_change(sym) for sym, name in INDICES.items()},
        "sectors": {name: _pct_change(sym) for sym, name in SECTORS.items()},
        "movers": [_pct_change(t) for t in TOP_TICKERS],
    }
