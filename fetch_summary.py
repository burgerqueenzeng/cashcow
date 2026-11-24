"""
CLI entry point: fetch today's market data and print a summary.
Used by the Orca automation — no API key required.
"""

from analysis.fetch import fetch_market_data
from analysis.summarize import build_summary

if __name__ == "__main__":
    market = fetch_market_data()
    print(build_summary(market))
