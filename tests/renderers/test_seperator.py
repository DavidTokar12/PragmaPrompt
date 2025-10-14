from __future__ import annotations

from typing import Any

import pytest

from pragma_prompt import separator
from pragma_prompt.runtime_context import session


CASES: list[tuple[dict[str, Any], str, str, str]] = [
    (
        {},
        "Without a title, returns a line of 8 '-' characters.",
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
        "Centers the title padded by '-' at default width 8.",
        f"{'-'*35} CONTEXT {'-'*36}",
        "title_default",
    ),
    (
        {"title": "BOX", "boxed": True, "char": "-", "width": 12},
        "With boxed=True, wraps the centered title between full-width lines.",
        "------------\n--- BOX ----\n------------",
        "title_boxed",
    ),
    (
        {"title": "X", "char": "*", "width": 9},
        "Centers the title using '*' with a total width of 9.",
        "*** X ***",
        "title_custom_char",
    ),
    (
        {"width": 2},  # clamped to minimum width 3
        "Width < 3 is clamped up to 3.",
        "---",
        "clamp_width",
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
