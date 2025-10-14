from __future__ import annotations

from typing import overload

from pragma_prompt.renderers.render_function import render_function


@overload
def separator() -> str: ...
@overload
def separator(title: str, *, char: str = "-", width: int = 80) -> str: ...


@render_function("separator")
def separator(
    title: str | None = None,
    *,
    char: str = "-",
    width: int = 80,
) -> str:
    """Render a visual divider line, optionally with a centered title.

    Args:
        title: Optional title to center within the divider.
        char: The character used to draw the divider line.
        width: Target width of the divider.

    Returns:
        The divider string.
    """
    if not title:
        return char * width

    title_with_padding = f" {title} "
    return title_with_padding.center(width, char)
