from __future__ import annotations

import pytest

from pragma_prompt.exceptions import LoaderError
from tests.includes.unclosed_sections.module import UnclosedModule


def test_render_with_unclosed_sections_raises_loader_error() -> None:
    with pytest.raises(LoaderError):
        UnclosedModule.prompt_unclosed.render()
