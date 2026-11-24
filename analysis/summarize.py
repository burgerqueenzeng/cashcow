"""Convert raw market data into a human-readable text summary for the LLM."""


def _fmt(item: dict) -> str:
    sign = "+" if (item["change_pct"] or 0) >= 0 else ""
    return f"{item['ticker']} {item['close']} ({sign}{item['change_pct']}%)"


def build_summary(market: dict) -> str:
    lines = [f"Date: {market['date']}", "", "## Indices"]
    for name, item in market["indices"].items():
        lines.append(f"  {name}: {_fmt(item)}")

    lines += ["", "## Sector Performance"]
    sectors_sorted = sorted(
        market["sectors"].items(),
        key=lambda x: x[1]["change_pct"] or 0,
        reverse=True,
    )
    for name, item in sectors_sorted:
        lines.append(f"  {name}: {_fmt(item)}")

    lines += ["", "## Notable Stocks"]
    for item in sorted(market["movers"], key=lambda x: x["change_pct"] or 0, reverse=True):
        lines.append(f"  {_fmt(item)}")

    return "\n".join(lines)
