"""
Prediction scorecard — tracks yesterday's prediction vs today's actual result.
Builds public credibility over time ("called it 7/10 days this month").
"""

import json
import os
from datetime import date, timedelta

SCORECARD_FILE = "reports/scorecard.json"


def load_scorecard() -> list:
    if not os.path.exists(SCORECARD_FILE):
        return []
    with open(SCORECARD_FILE) as f:
        return json.load(f)


def save_scorecard(records: list):
    os.makedirs("reports", exist_ok=True)
    with open(SCORECARD_FILE, "w") as f:
        json.dump(records, f, indent=2)


def record_prediction(prediction_text: str, spy_direction: str):
    """Call this after generating today's review. spy_direction: 'up'|'down'|'flat'"""
    records = load_scorecard()
    records.append({
        "date": date.today().isoformat(),
        "prediction": prediction_text,
        "predicted_direction": spy_direction,
        "actual_direction": None,
        "correct": None,
    })
    save_scorecard(records)


def verify_yesterday(actual_spy_change_pct: float):
    """Call at start of each day to score yesterday's prediction."""
    records = load_scorecard()
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    for r in records:
        if r["date"] == yesterday and r["actual_direction"] is None:
            if actual_spy_change_pct > 0.3:
                actual = "up"
            elif actual_spy_change_pct < -0.3:
                actual = "down"
            else:
                actual = "flat"
            r["actual_direction"] = actual
            r["correct"] = r["predicted_direction"] == actual
    save_scorecard(records)


def monthly_summary() -> str:
    records = load_scorecard()
    scored = [r for r in records if r["correct"] is not None]
    if not scored:
        return "No scored predictions yet."
    correct = sum(1 for r in scored if r["correct"])
    return f"Prediction accuracy: {correct}/{len(scored)} ({round(correct/len(scored)*100)}%) this period"
