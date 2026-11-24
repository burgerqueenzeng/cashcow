"""Format the generated review for each platform."""


def format_rednote(review: dict) -> str:
    """Return ready-to-paste Rednote post."""
    return review.get("rednote", "")


def format_x(review: dict) -> list[str]:
    """Return list of tweets for a thread."""
    x_raw = review.get("x_thread", "")
    tweets = []
    for line in x_raw.splitlines():
        line = line.strip()
        if line and line[0] == "[" and "]" in line:
            tweet = line.split("]", 1)[1].strip()
            if tweet:
                tweets.append(tweet)
    return tweets
