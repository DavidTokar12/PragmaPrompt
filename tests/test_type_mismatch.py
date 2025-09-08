from __future__ import annotations

import types

import pytest

from prompt_craft_kit.exceptions import LoaderError
from tests.includes.type_mismatch.module import TypedModule


def test_render_model_type_mismatch_raises_loader_error() -> None:
    good_ctx = types.SimpleNamespace(project="ok")
    with pytest.raises(LoaderError):
        TypedModule.mismatch_prompt.render(context=good_ctx, render_model=123)


def test_context_type_mismatch_raises_loader_error() -> None:
    good_rm = types.SimpleNamespace(name="ok")
    with pytest.raises(LoaderError):
        TypedModule.mismatch_prompt.render(
            context={"project": "x"}, render_model=good_rm
        )
