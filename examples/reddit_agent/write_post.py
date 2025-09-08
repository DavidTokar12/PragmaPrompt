from __future__ import annotations

import prompt_craft_kit as pck

from examples.reddit_agent.module import RedditAgent
from examples.reddit_agent.module import RedditComponents


rm = RedditAgent.write_post.render_model

"""
You are drafting a Reddit thread. Keep it short, vivid, and dank.
Make sure to offend as many people as possible to trigger a response.
"""

RedditComponents.platform_rules.render()
RedditComponents.safety_disclaimer.render()

with pck.section("context"):
    f"subreddit: {rm.subreddit}"
    f"theme: {rm.theme}"
    f"audience: {rm.audience}"

with pck.section("constraints"):
    pck.bullets(
        {
            "max_length": "~1400 chars",
            "links": "Optional; include one if truly helpful",
            "flair": "From the allowed list only (see below)",
        }
    )

with pck.section("allowed-flares"):
    pck.bullets(
        [
            "Discussion",
            "Unpopular Opinion",
            "Serious",
            "Satire",
            "Debate",
        ]
    )

with pck.section("engagement-signals"):
    pck.table(
        rows=[
            ("upvotes", "measure raw visibility"),
            ("replies", "indicates provocation success"),
            ("deltas", "tracks persuasion / mind-change"),
            ("reports", "optional, shows if it went too far"),
        ],
        headers=["signal", "meaning"],
        fmt="csv",
    )

with pck.section("output_example"):
    pck.output_example(
        {
            "title": "Pineapple on pizza is the future of Italian cuisine",
            "body_markdown": (
                "Italians act like pineapple on pizza is cultural vandalism, "
                "but let's be honest: it's actually gourmet. "
                "The sweetness balances the salt, the texture pops, "
                "and if you can't handle that, maybe you're just stuck in the past. "
                "Try it before crying to your nonna."
            ),
            "flair": "Unpopular Opinion",
        },
        comments={
            "title": "bold claim up front to trigger reactions",
            "body_markdown": "target Italians directly, call pineapple 'gourmet', mock tradition to maximize replies",
        },
    )
