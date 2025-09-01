from __future__ import annotations

from typing import overload

from prompt_craft_kit.renderers.render_function import render_function
from prompt_craft_kit.renderers.renderers import Renderers


@overload
def separator() -> str: ...


@overload
def separator(
    title: str, *, char: str = "-", width: int = 80, boxed: bool = False
) -> str: ...


@render_function(Renderers.SEPARATOR)
def separator(
    title: str | None = None,
    *,
    char: str = "-",
    width: int = 80,
    boxed: bool = False,
) -> str:
    """
    Visual divider. Examples:
      separator()
      separator("CONTEXT", char="=")
      separator("CONTEXT", boxed=True)
    """

    if width < 3:
        width = 3

    line = char * width

    if not title:
        return line

    title_with_padding = f" {title} "
    centered = title_with_padding.center(width, char)

    if boxed:
        return f"{line}\n{centered}\n{line}"

    return centered
