from __future__ import annotations

import pytest

import pragma_prompt as pp

from pragma_prompt.runtime_context import _ALLOW_RENDERERS
from pragma_prompt.runtime_context import _allow_renderer_outside_prompt


def test_renderer_outside_prompt_requires_session() -> None:
    _ALLOW_RENDERERS.set(False)
    with pytest.raises(RuntimeError):
        pp.warning("hi")
    _ALLOW_RENDERERS.set(False)


def test_renderer_outside_prompt_allowed_after_opt_in() -> None:
    _ALLOW_RENDERERS.set(False)
    _allow_renderer_outside_prompt()
    out = pp.warning("hi")
    assert out == "<NOTICE>\nhi\n</NOTICE>"
    _ALLOW_RENDERERS.set(False)
