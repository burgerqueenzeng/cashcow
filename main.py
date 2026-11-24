"""
CashCow - Daily US market review generator.
Run after market close (US Eastern time).
"""

import os
from datetime import date
from dotenv import load_dotenv

from analysis.fetch import fetch_market_data
from analysis.summarize import build_summary
from publisher.generate import generate_review
from publisher.format import format_rednote, format_x

load_dotenv()


def run():
    today = date.today().isoformat()
    print(f"[CashCow] Running for {today}")

    print("Fetching market data...")
    market = fetch_market_data()

    print("Building summary...")
    summary = build_summary(market)

    print("Generating review via Claude...")
    review = generate_review(summary)

    # Save raw report
    os.makedirs("reports", exist_ok=True)
    report_path = f"reports/{today}.md"
    with open(report_path, "w") as f:
        f.write(review["full"])
    print(f"Report saved: {report_path}")

    print("\n--- Rednote (小红书) ---")
    print(format_rednote(review))

    print("\n--- X (Twitter thread) ---")
    for i, tweet in enumerate(format_x(review), 1):
        print(f"[{i}] {tweet}\n")


if __name__ == "__main__":
    run()
