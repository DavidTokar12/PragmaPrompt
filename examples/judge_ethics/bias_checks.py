from __future__ import annotations

import prompt_craft_kit as pck


pck.warning(
    title="Bias checks",
    level=2,
    body=(
        "Actively look for confirmation bias, anchoring, and selection bias.\n"
        "If bias detected, state it and compensate."
    ),
)
