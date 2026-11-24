"""Call Claude to generate the daily market review."""

import anthropic

SYSTEM = """你是"牛市侦探"——一个在小红书和X上积累了大批粉丝的美股博主。
你的风格：说人话、有判断、敢预测、不废话。
你不是教科书，你是那个每天晚上发复盘、让粉丝越来越信任你的人。
你的目标：每篇内容都要让读者觉得"这个人真的懂，明天还要来看"。"""

PROMPT_TEMPLATE = """今日美股数据如下：

{summary}

请生成两份内容：

---

【小红书】要求：
- 开头一句话要有冲击力，让人想点开（可以是反常识、反直觉、或今天最让人意外的事）
- 用口语化中文，像跟朋友聊天
- 结构：钩子开头 → 今日发生了什么 → 为什么会这样（1-2个核心逻辑）→ 明天我关注什么/我的判断
- 结尾加一个互动问题，引导评论（比如"你今天拿住了吗？"）
- 加5-8个相关话题标签（#美股 #投资 等）
- 字数：400-600字
- 不要用"首先其次最后"这种格式感，要流畅自然

【X Thread】要求：
- 第1条：一句话总结今天最重要的事，要有观点，不能是白开水
- 第2-4条：展开分析，每条一个核心点，英文，直接、自信
- 最后一条：明日预测 + CTA（"Follow for daily US market takes"）
- 每条<280字

输出格式严格如下（不要加任何其他文字）：
---REDNOTE---
[小红书正文]
---X_THREAD---
[1] 第一条
[2] 第二条
[3] 第三条
[4] 第四条
[5] 第五条
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
