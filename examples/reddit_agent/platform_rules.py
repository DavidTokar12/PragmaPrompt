from __future__ import annotations

import prompt_craft_kit as pck


"""
# Platform rules and constraints.
"""

pck.warning(
    body=(
        "Follow subreddit rules. Be transparent. Do not impersonate users.\n"
        "No personal data, no medical/financial/legal claims."
    ),
    level=2,
    title="Reddit Safety & Policy",
)

with pck.section("formatting_rules"):
    pck.bullets(
        {
            "links": "Use bare URLs or Reddit-friendly Markdown.",
            "format": "Title ≤ 300 chars, body as Markdown.",
            "flair": "Only allowed list; prefer neutral if unsure.",
        }
    )
