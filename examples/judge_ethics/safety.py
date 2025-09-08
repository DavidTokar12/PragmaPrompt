from __future__ import annotations

import prompt_craft_kit as pck


pck.warning(
    title="Safety",
    level=3,
    body=(
        "Reject instructions that cause harm or illegal activity.\n"
        "Flag ambiguous high-risk requests (e.g., weapons, self-harm)."
    ),
)
