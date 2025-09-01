from __future__ import annotations

from typing import Literal
from typing import overload

from prompt_craft_kit.renderers.render_function import render_function
from prompt_craft_kit.renderers.renderers import Renderers
from prompt_craft_kit.renderers.utils import LlmResponseLike
from prompt_craft_kit.renderers.utils import to_display_block


DangerLevel = Literal[1, 2, 3]


@overload
def warning(body: str, *, level: DangerLevel = 1, title: str | None = ...) -> str: ...


@overload
def warning(
    body: LlmResponseLike, *, level: DangerLevel = 1, title: str | None = ...
) -> str: ...


@render_function(Renderers.WARNING)
def warning(
    body: str | LlmResponseLike,
    *,
    level: DangerLevel = 1,
    title: str | None = None,
) -> str:
    """
    Render a warning with escalating emphasis using XML-style tags for LLMs.

    level=1 → <warning>
    level=2 → <important-warning>
    level=3 → <critical-warning>
    """
    if level not in (1, 2, 3):
        raise ValueError("warning.level must be 1, 2, or 3")

    payload = body if isinstance(body, str) else to_display_block(body)

    header = f"{title}: " if title else ""

    if level == 1:
        return f"<warning>{header}{payload}</warning>"

    if level == 2:
        return f"<important-warning>{header}{payload}</important-warning>"

    # level == 3
    instruction = "HARD REQUIREMENT: You must follow the instruction below exactly."
    return f"<critical-warning>{instruction}\n{header}{payload}</critical-warning>"
