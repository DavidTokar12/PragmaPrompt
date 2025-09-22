from __future__ import annotations

import pragma_prompt as pp


"""
# Platform rules and constraints.
"""

pp.warning(
    body=(
        "Follow subreddit rules. Be transparent. Do not impersonate users.\n"
        "No personal data, no medical/financial/legal claims."
    ),
    level=2,
    title="Reddit Safety & Policy",
)

with pp.section("formatting_rules"):
    pp.bullets(
        {
            "links": "Use bare URLs or Reddit-friendly Markdown.",
            "format": "Title ≤ 300 chars, body as Markdown.",
            "flair": "Only allowed list; prefer neutral if unsure.",
        }
    )
