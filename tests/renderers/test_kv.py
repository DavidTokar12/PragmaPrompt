from __future__ import annotations

from typing import Any

import pytest

from pragma_prompt import bullets
from pragma_prompt.runtime_context import session


CASES: list[tuple[dict[str, Any], str, str, str]] = [
    (
        {"items": {"role": "analyst", "expertise": "finance", "years": 10}},
        "Should render a dictionary (mapping) as a Markdown list.",
        "- role: analyst\n- expertise: finance\n- years: 10",
        "dict_input",
    ),
    (
        {
            "items": [
                ("system", "You are a helpful assistant."),
                ("user", "Please summarize this document."),
            ]
        },
        "Should render a list of tuples (sequence) as a Markdown list.",
        "- system: You are a helpful assistant.\n- user: Please summarize this document.",
        "list_of_tuples_input",
    ),
    (
        {
            "items": [
                "Discussion",
                "Unpopular Opinion",
                "Serious",
                "Satire",
                "Debate",
            ]
        },
        "Should render a plain list of values as a bullet list.",
        "- Discussion\n- Unpopular Opinion\n- Serious\n- Satire\n- Debate",
        "plain_list_input",
    ),
]


@pytest.mark.parametrize(
    "kwargs, description, expected, case", CASES, ids=[c[-1] for c in CASES]
)
def test_bullets_cases(
    kwargs: dict[str, Any],
    description: str,
    expected: str,
    case: str,
) -> None:
    """
    Tests the bullets function for both dictionary and list inputs by comparing
    the output to an exact expected string.
    """
    with session(constants=None, context=None, render_model=None):
        out = bullets(**kwargs)
        assert out == expected
