from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import ParamSpec

from pragma_prompt.renderers.render_plan import build_render_call
from pragma_prompt.runtime_context import add_render_call


P = ParamSpec("P")


def render_function(renderer: str) -> Callable[[Callable[P, str]], Callable[P, str]]:
    """
    Decorate a renderer that returns `str` so that calling it will:
      1) run the renderer, 2) capture the call details/result in the render plan,
      3) return the same str to the caller.
    """

    def _wrap(func: Callable[P, str]) -> Callable[P, str]:
        @wraps(func)
        def _inner(*args: P.args, **kwargs: P.kwargs) -> str:
            body = func(*args, **kwargs)
            call = build_render_call(
                renderer=renderer,
                func=func,
                args=args,
                kwargs=kwargs,
                result=body,
            )
            add_render_call(call)
            return body

        return _inner

    return _wrap
