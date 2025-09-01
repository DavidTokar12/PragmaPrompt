from __future__ import annotations

from typing import Any

import pytest

from prompt_craft_kit import kv
from prompt_craft_kit.runtime_context import session


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
]


@pytest.mark.parametrize(
    "kwargs, description, expected, case", CASES, ids=[c[-1] for c in CASES]
)
def test_kv_cases(
    kwargs: dict[str, Any],
    description: str,
    expected: str,
    case: str,
) -> None:
    """
    Tests the kv function for both dictionary and list inputs by comparing
    the output to an exact expected string.
    """
    with session(constants=None, context=None, render_model=None):
        out = kv(**kwargs)
        assert out == expected
