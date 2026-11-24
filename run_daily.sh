#!/bin/bash
# CashCow daily market review — runs locally via Claude Code CLI
# Triggered by crontab at 4:33 PM ET (Mon-Fri)

set -e
cd "$(dirname "$0")"

# Fetch market data
pip3 install yfinance pandas --quiet > /dev/null 2>&1
SUMMARY=$(python3 fetch_summary.py)

# Generate review with local Claude Code
DATE=$(date +%Y-%m-%d)
REPORT_FILE="reports/${DATE}.md"
mkdir -p reports

PROMPT="You are CashCow (牛市侦探), a punchy opinionated Chinese-American stock market blogger.

Today's market data:
${SUMMARY}

Write TWO pieces of content:

--- REDNOTE (小红书) ---
400-600 Chinese characters. Surprising/contrarian hook as first line. Conversational Mandarin. Flow: hook → what happened → why (1-2 logic points) → my call for tomorrow. End with engagement question. Add 5-8 hashtags (#美股 #投资 #理财 etc).

--- X THREAD ---
5 tweets, each under 280 English chars. Tweet 1: most important thing today, opinionated. Tweets 2-4: one insight each. Tweet 5: tomorrow prediction + 'Follow for daily US market takes'.

Print both labeled clearly."

echo "$PROMPT" | /opt/homebrew/bin/claude --print --model claude-haiku-4-5-20251001 | tee "$REPORT_FILE"

echo ""
echo "Saved to $REPORT_FILE"
