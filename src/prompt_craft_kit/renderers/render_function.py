from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import ParamSpec

from prompt_craft_kit.renderers.prompt_section import PromptSection
from prompt_craft_kit.renderers.renderers import Renderers
from prompt_craft_kit.runtime_context import add_section


P = ParamSpec("P")


def render_function(
    renderer: Renderers,
) -> Callable[[Callable[P, str]], Callable[P, str]]:
    """
    Decorate a renderer that returns `str` so that calling it will:
      1) run the renderer, 2) wrap result as PromptSection, 3) append it,
      4) return the same str to the caller.
    """

    def _wrap(func: Callable[P, str]) -> Callable[P, str]:
        @wraps(func)
        def _inner(*args: P.args, **kwargs: P.kwargs) -> str:
            body = func(*args, **kwargs)
            add_section(
                PromptSection(body=body, renderer=renderer, input_params=dict(kwargs))
            )
            return body

        return _inner

    return _wrap
