"""Call Claude to generate the daily market review."""

import anthropic

SYSTEM = """你是一个在小红书和X上有真实粉丝的美股博主，风格参考MentoviaX但用中文写作。

你的写作原则：
1. 情绪先行。不用数据开头，用感受开头——让读者先感受到今天市场的重量
2. 数字要有历史锚点。不说"跌了很多"，说"这是自2020年3月疫情以来最惨的一周"
3. 个人透明。偶尔透露自己的仓位感受或判断，让读者觉得你和他们在一起扛
4. 哲学转折。从数据分析转向投资心态和mindset，把自己变成导师而不只是分析师
5. 集体感。用"我们"，不是"你们"——你是和读者一起经历市场的人
6. 敢给具体level。给出明确的关键价位，让付费内容感觉值得
7. 节奏感。短句+停顿，像在说话，不像在写报告
8. 目标：让读者读完觉得"这个人真的经历过市场，不是在纸上谈兵"，明天还要来看"""

PROMPT_TEMPLATE = """今日美股数据如下：

{summary}

请生成两份内容：

---

【小红书】要求（500-700字）：
- 情绪开头：用一句有冲击力的话描述今天的市场感受，不是数据
- 然后给出关键数字，但每个数字配上历史对比（"这是自XX以来最XX"）
- 中段：解释为什么会这样，1-2个核心逻辑，说人话
- 转折：从市场分析转向投资心态/mindset，像导师在说话
- 给出明天具体要关注的价位或信号
- 结尾：互动问题（"你今天拿住了吗？"/"你是加仓了还是跑了？"）
- 5-8个话题标签（#美股 #投资 #理财 等）
- 口语化，流畅，不用"首先其次最后"，用省略号"……"作停顿

【X Thread】要求（5条，每条<280字）：
- 第1条：一句话说今天最重要的事，要有历史对比，要有情绪重量
- 第2-3条：数据+分析，每条一个核心点，直接自信
- 第4条：mindset/投资哲学，一两句话，有深度
- 第5条：明日关键level/信号 + "Follow for daily US market takes"

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
        model="claude-haiku-4-5-20251001",
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
