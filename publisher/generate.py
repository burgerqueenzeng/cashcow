"""Call Claude to generate the daily market review."""

import anthropic

SYSTEM = """你是一位专业的美股市场分析师，擅长用简洁易懂的中文为普通投资者解读市场。
你的分析风格：客观、有洞见、偶尔幽默，不夸大也不恐慌。
每次分析包含：当日市场回顾、关键驱动因素、明日展望与操作建议。"""

PROMPT_TEMPLATE = """根据以下今日美股数据，请生成：

1. 一篇完整的市场日评（中文，500-800字），适合小红书发布
2. 一个推特发帖串（英文，5条以内，每条<280字），适合X发布

市场数据：
{summary}

输出格式：
---REDNOTE---
[小红书正文]
---X_THREAD---
[1] 第一条推文
[2] 第二条推文
...
---END---
"""


def generate_review(summary: str) -> dict:
    client = anthropic.Anthropic()
    prompt = PROMPT_TEMPLATE.format(summary=summary)

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2048,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text
    return _parse(raw, summary)


def _parse(raw: str, summary: str) -> dict:
    rednote, x_thread = "", ""

    if "---REDNOTE---" in raw and "---X_THREAD---" in raw:
        rednote = raw.split("---REDNOTE---")[1].split("---X_THREAD---")[0].strip()
        x_thread = raw.split("---X_THREAD---")[1].split("---END---")[0].strip()
    else:
        rednote = raw
        x_thread = ""

    return {"full": f"# Market Review\n\n{summary}\n\n---\n\n{raw}", "rednote": rednote, "x_thread": x_thread}
