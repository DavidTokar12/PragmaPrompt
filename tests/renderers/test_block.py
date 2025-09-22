from __future__ import annotations

from typing import Any

import pytest

from pragma_prompt import block
from pragma_prompt.runtime_context import session


CASES: list[tuple[dict[str, Any], str, str, str]] = [
    (
        {"content": "This is a simple block of text.\nIt can have multiple lines."},
        "The block renderer should return its input content unmodified.",
        "This is a simple block of text.\nIt can have multiple lines.",
        "simple_return",
    ),
]


@pytest.mark.llm
@pytest.mark.parametrize(
    "kwargs, description, expected, case", CASES, ids=[c[-1] for c in CASES]
)
def test_block_cases(
    kwargs: dict[str, Any],
    description: str,
    expected: str,
    case: str,
) -> None:
    """
    Tests the block function, comparing its output to an exact expected string.
    """
    with session(constants=None, context=None, render_model=None):
        out = block(**kwargs)
        assert out == expected
