from __future__ import annotations

from typing import Any

import pytest

from pragma_prompt import separator
from pragma_prompt.runtime_context import session


CASES: list[tuple[dict[str, Any], str, str, str]] = [
    (
        {},
        "Without a title, returns a line of 80 '-' characters.",
        "-" * 80,
        "no_args_default",
    ),
    (
        {"char": "=", "width": 10},
        "Uses the provided char '=' and width=10 when no title is given.",
        "=" * 10,
        "char_width_no_title",
    ),
    (
        {"title": "CONTEXT"},
        "Centers the title padded by '-' at default width 80.",
        " CONTEXT ".center(80, "-"),
        "title_default",
    ),
    (
        {"title": "X", "char": "*", "width": 9},
        "Centers the title using '*' with a total width of 9.",
        "*** X ***",
        "title_custom_char",
    ),
    (
        {"width": 2},
        "Width can be less than 3.",
        "--",
        "width_less_than_3",
    ),
]


@pytest.mark.parametrize(
    "kwargs, description, expected, case", CASES, ids=[c[-1] for c in CASES]
)
def test_separator_cases(
    kwargs: dict[str, Any],
    description: str,
    expected: str,
    case: str,
) -> None:
    with session(constants=None, context=None, render_model=None):
        out = separator(**kwargs)
        assert out == expected, f"Output did not match expectation for case '{case}'."
