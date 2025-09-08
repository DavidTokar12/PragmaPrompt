from __future__ import annotations

import textwrap

from prompt_craft_kit.renderers.render_function import render_function


@render_function("block")
def block(content: str) -> str:
    """Render a simple text block.

    Dedents and strips the given string so it can be embedded cleanly in a prompt.

    Args:
        content: Arbitrary text content (leading indentation and surrounding
            whitespace are removed).

    Returns:
        The normalized text (dedented + stripped).
    """
    normalized = textwrap.dedent(content).strip()
    return normalized  # (BUGFIX: no trailing comma)
