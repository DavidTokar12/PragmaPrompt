from __future__ import annotations

from typing import Any

import pytest

from pragma_prompt import warning
from pragma_prompt.runtime_context import session


CASES: list[tuple[dict[str, Any], str, str, str]] = [
    (
        {"body": "The system is overheating.", "level": 1},
        "A level 1 warning should use a <NOTICE> tag with newline-wrapped content.",
        "<NOTICE>\nThe system is overheating.\n</NOTICE>",
        "level_1_default_tag",
    ),
    (
        {
            "body": "API keys will expire in 24 hours.",
            "level": 2,
            "title": "Expiration Notice",
        },
        "A level 2 warning should use a <WARNING> tag with a title and newline-wrapped content.",
        "<WARNING>\nExpiration Notice: API keys will expire in 24 hours.\n</WARNING>",
        "level_2_custom_title_tag",
    ),
    (
        {"body": "Do not output any personal identifying information.", "level": 3},
        "A level 3 warning should use a <CONSTRAINT> tag with newline-wrapped content.",
        "<CONSTRAINT>\nDo not output any personal identifying information.\n</CONSTRAINT>",
        "level_3_critical_tag",
    ),
    (
        {"body": ["alpha", "beta"], "level": 1},
        "Structured bodies such as lists should be rendered as pretty JSON inside the <NOTICE> tag.",
        '<NOTICE>\n[\n  "alpha",\n  "beta"\n]\n</NOTICE>',
        "structured_list_body",
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
