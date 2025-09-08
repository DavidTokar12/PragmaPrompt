from __future__ import annotations

import prompt_craft_kit as pck

from examples.reddit_agent.module import RedditAgent
from examples.reddit_agent.module import RedditComponents


ctx = RedditAgent.write_replies.context
rm = RedditAgent.write_replies.render_model

"""
Generate short, kind replies for a thread. This shows: section(), shot(), bullets(),
separator(), and a tiny block() usage.
"""

RedditComponents.brand_voice.render()
RedditComponents.platform_rules.render()


with pck.section("context"):
    f"subreddit: {ctx.subreddit}"
    f"theme: {ctx.theme}"
    f"audience: {ctx.audience}"

pck.separator("REPLY EXAMPLES")

pck.shot(
    user="User: 'This is obviously fake.'",
    thought="De-escalate, bring data if available, invite constructive chat.",
    output=(
        "I hear you—skepticism is healthy. I couldn’t verify the stat, so I left it out."
    ),
)

pck.shot(
    user="User: 'Tabs over spaces forever.'",
    output="I use both. Tabs for chaos, spaces for therapy. We can be friends.",
)

with pck.section("constraints"):
    pck.kv(
        {
            "max_replies": 3,
            "style": "warm + concise",
            "avoid": "arguing or piling on",
        }
    )

pck.separator("OUTPUT FORMAT")

pck.output_format(
    {
        "replies": [
            {
                "reply_markdown": "",
                "mood": "friendly|neutral",
                "safety_notes": [],
            }
        ]
    }
)

# Tiny explicit block usage (usually triple-quoted strings already cover this)
pck.block("Return only the <replies> section below.")

with pck.section("replies"):
    """
    <reply>
      <text>...</text>
      <mood>...</mood>
    </reply>
    ... up to 3
    """
