from __future__ import annotations

import pragma_prompt as pp


# A short, high-priority guardrail (level=3 adds an explicit hard requirement)
pp.warning(
    body=(
        "Do not fabricate facts or statistics. Cite or say 'can't verify'.\n"
        "No harassment, hate, or personal attacks under any circumstances."
    ),
    title="Hard Safety Rule",
    level=3,
)
