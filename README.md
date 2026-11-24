# CashCow

A daily US stock market observation and analysis system.

## What it does

- **Observes** key US market data every trading day (indices, sectors, movers)
- **Writes** a daily market review in Mandarin + English
- **Predicts** next-day outlook based on technicals, sentiment, and macro signals
- **Publishes** posts formatted for Rednote and X (Twitter)

## Project Structure

```
cashcow/
├── data/           # Raw market data fetched daily
├── analysis/       # Analysis scripts (technicals, sentiment, macro)
├── reports/        # Generated daily review files
├── publisher/      # Formatters for Rednote & X
├── prompts/        # LLM prompt templates for review generation
└── scheduler/      # Cron / automation entry points
```

## Daily Flow

1. Fetch market close data (indices, top movers, sector performance, VIX)
2. Run analysis (trend, momentum, breadth)
3. Generate Mandarin review + next-day prediction via LLM
4. Format for Rednote (long-form) and X (thread)
5. Save to `reports/YYYY-MM-DD.md`

## Stack

- Python 3.11+
- `yfinance` for market data
- Claude API for review generation
- GitHub Actions for daily scheduling

## Getting Started

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in your API keys
python main.py
```
