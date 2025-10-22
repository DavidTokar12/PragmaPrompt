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
    """Render a warning block with escalating emphasis using XML-style tags.

    Levels:
        1 → ``<NOTICE>…</NOTICE>``
        2 → ``<WARNING>…</WARNING>``
        3 → ``<CONSTRAINT>…</CONSTRAINT>``

    Args:
        body: Warning text or displayable content (string, mapping, dataclass, model,
            or nested list of those types).
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

    tag_by_level = {
        1: "NOTICE",
        2: "WARNING",
        3: "CONSTRAINT",
    }
    tag = tag_by_level[level]
    header = f"{title}: " if title else ""

    return f"<{tag}>\n{header}{payload}\n</{tag}>"
