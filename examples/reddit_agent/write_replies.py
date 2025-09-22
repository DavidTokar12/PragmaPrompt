from __future__ import annotations

import pragma_prompt as pp

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


with pp.section("context"):
    f"subreddit: {ctx.subreddit}"
    f"theme: {ctx.theme}"
    f"audience: {ctx.audience}"

pp.separator("REPLY EXAMPLES")

pp.shot(
    user="User: 'This is obviously fake.'",
    thought="De-escalate, bring data if available, invite constructive chat.",
    output=(
        "I hear you—skepticism is healthy. I couldn't verify the stat, so I left it out."
    ),
)

pp.shot(
    user="User: 'Tabs over spaces forever.'",
    output="I use both. Tabs for chaos, spaces for therapy. We can be friends.",
)

with pp.section("constraints"):
    pp.kv(
        {
            "max_replies": 3,
            "style": "warm + concise",
            "avoid": "arguing or piling on",
        }
    )

pp.separator("OUTPUT FORMAT")

pp.output_format(
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
pp.block("Return only the <replies> section below.")

with pp.section("replies"):
    """
    <reply>
      <text>...</text>
      <mood>...</mood>
    </reply>
    ... up to 3
    """
