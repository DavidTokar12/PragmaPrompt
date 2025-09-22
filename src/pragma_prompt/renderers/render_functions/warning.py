from __future__ import annotations

from typing import Literal
from typing import overload

from pragma_prompt.renderers.render_function import render_function
from pragma_prompt.renderers.types import LlmResponseLike
from pragma_prompt.renderers.utils import to_display_block


DangerLevel = Literal[1, 2, 3]


@overload
def warning(body: str, *, level: DangerLevel = 1, title: str | None = ...) -> str: ...
@overload
def warning(
    body: LlmResponseLike, *, level: DangerLevel = 1, title: str | None = ...
) -> str: ...


@render_function("warning")
def warning(
    body: str | LlmResponseLike,
    *,
    level: DangerLevel = 1,
    title: str | None = None,
) -> str:
    """Render a warning with escalating emphasis using XML-style tags.

    Levels:
        1 → ``<WARNING>…</WARNING>``
        2 → ``<IMPORTANT-WARNING>…</IMPORTANT-WARNING>``
        3 → ``<CRITICAL-WARNING>…</CRITICAL-WARNING>`` (prepends a hard-requirement line)

    Args:
        body: Warning text or displayable content.
        level: Severity level (1, 2, or 3).
        title: Optional title prepended to the message.

    Returns:
        The formatted warning string.

    Raises:
        ValueError: If ``level`` is not 1, 2, or 3.
    """
    if level not in (1, 2, 3):
        raise ValueError("warning.level must be 1, 2, or 3")

    payload = body if isinstance(body, str) else to_display_block(body)
    header = f"{title}: " if title else ""

    if level == 1:
        tag = "WARNING"
        return f"<{tag}>\n{header}{payload}\n</{tag}>"
    if level == 2:
        tag = "IMPORTANT-WARNING"
        return f"<{tag}>\n{header}{payload}\n</{tag}>"

    # level == 3
    tag = "CRITICAL-WARNING"
    instruction = "HARD REQUIREMENT: You must follow the instruction below exactly."
    return f"<{tag}>\n{instruction}\n{header}{payload}\n</{tag}>"
