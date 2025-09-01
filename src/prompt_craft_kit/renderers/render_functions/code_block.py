from __future__ import annotations

from prompt_craft_kit.renderers.render_function import render_function
from prompt_craft_kit.renderers.renderers import Renderers


@render_function(Renderers.CODE)
def code_block(code: str, lang: str) -> str:
    """
    Fenced code block (Markdown).
    """
    fence = "```" + (lang)
    return f"{fence}\n{code}\n```"
