from __future__ import annotations

import pragma_prompt as pp

from examples.reddit_agent.module import RedditAgent
from examples.reddit_agent.module import RedditComponents


rm = RedditAgent.write_post.render_model

"""
You are drafting a Reddit thread. Keep it short, vivid, and dank.
Make sure to offend as many people as possible to trigger a response.
"""

RedditComponents.platform_rules.render()
RedditComponents.safety_disclaimer.render()

with pp.section("context"):
    f"subreddit: {rm.subreddit}"
    f"theme: {rm.theme}"
    f"audience: {rm.audience}"

with pp.section("constraints"):
    pp.bullets(
        {
            "max_length": "~1400 chars",
            "links": "Optional; include one if truly helpful",
            "flair": "From the allowed list only (see below)",
        }
    )

with pp.section("allowed-flares"):
    pp.bullets(
        [
            "Discussion",
            "Unpopular Opinion",
            "Serious",
            "Satire",
            "Debate",
        ]
    )

with pp.section("engagement-signals"):
    pp.table(
        rows=[
            ("upvotes", "measure raw visibility"),
            ("replies", "indicates provocation success"),
            ("deltas", "tracks persuasion / mind-change"),
            ("reports", "optional, shows if it went too far"),
        ],
        headers=["signal", "meaning"],
        fmt="csv",
    )

with pp.section("output_example"):
    pp.output_example(
        {
            "title": "Hot take: every CS major should fail a class on purpose",
            "body_markdown": (
                "If you haven't bombed a class yet, you're not learning. "
                "Recruiters trust resilience more than a 4.0 GPA. "
                "Tank algorithms, brag about the growth arc, and you'll ace the vibe checks. "
                "Stop flexing perfect transcripts and start flexing scar tissue."
            ),
            "flair": "Discussion",
        },
        comments={
            "title": "bold provocation that drags in every overachiever",
            "body_markdown": "call out perfectionism, push failure-as-flex narrative, keep it cocky + motivational",
        },
    )
