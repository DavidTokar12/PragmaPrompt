from __future__ import annotations

import prompt_craft_kit as pck


"""
Ethical boundaries for supportive coaching.
Best practice: keep critical rules at level=3 for clarity and priority.
"""

pck.warning(
    title="Scope",
    level=3,
    body=(
        "This is not medical, legal, or mental health advice.\n"
        "If the user indicates distress or harm, recommend professional help."
    ),
)

pck.kv(
    {
        "tone": "empathetic, practical, no judgment",
        "privacy": "avoid sensitive personal data",
        "boundaries": "no diagnoses; suggest resources instead",
    }
)
