from __future__ import annotations

from prompt_craft_kit.renderers.render_function import render_function
from prompt_craft_kit.renderers.renderers import Renderers


@render_function(Renderers.BLOCK)
def block(content: str) -> str:
    return content
