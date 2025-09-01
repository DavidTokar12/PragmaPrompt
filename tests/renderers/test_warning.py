from __future__ import annotations

from typing import Any

import pytest

from prompt_craft_kit import warning
from prompt_craft_kit.runtime_context import session


CASES: list[tuple[dict[str, Any], str, str, str]] = [
    (
        {"body": "The system is overheating.", "level": 1},
        "A level 1 warning should use a simple <warning> tag.",
        "<warning>The system is overheating.</warning>",
        "level_1_default_tag",
    ),
    (
        {
            "body": "API keys will expire in 24 hours.",
            "level": 2,
            "title": "Expiration Notice",
        },
        "A level 2 warning should use an <important-warning> tag with a title.",
        "<important-warning>Expiration Notice: API keys will expire in 24 hours.</important-warning>",
        "level_2_custom_title_tag",
    ),
    (
        {"body": "Do not output any personal identifying information.", "level": 3},
        "A level 3 warning should use a <critical-warning> tag with a hard requirement.",
        (
            "<critical-warning>HARD REQUIREMENT: You must follow the instruction below exactly.\n"
            "Do not output any personal identifying information.</critical-warning>"
        ),
        "level_3_critical_tag",
    ),
]


@pytest.mark.parametrize(
    "kwargs, description, expected, case", CASES, ids=[c[-1] for c in CASES]
)
def test_warning_cases(
    kwargs: dict[str, Any],
    description: str,
    expected: str,
    case: str,
) -> None:
    """
    Tests the warning function at all danger levels, comparing output to an exact expected string.
    """
    with session():
        out = warning(**kwargs)

    assert out == expected
