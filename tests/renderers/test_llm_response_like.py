from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import pytest

from pydantic import BaseModel

from prompt_craft_kit.renderers.utils import to_display_block


@dataclass
class SampleDataClass:
    name: str
    value: int


class SamplePydanticModel(BaseModel):
    name: str
    value: int


CASES: list[tuple[Any, str, str]] = [
    (
        "This is a plain string.",
        "A plain string that is not JSON should be returned unmodified.",
        "plain_string_input",
    ),
    (
        '{"key": "value", "is_json": true}',
        "A string containing valid JSON should be detected and pretty-printed.",
        "json_string_input",
    ),
    (
        SampleDataClass(name="dataclass_obj", value=123),
        "A dataclass instance should be serialized to pretty-printed JSON.",
        "dataclass_input",
    ),
    (
        SamplePydanticModel(name="pydantic_obj", value=456),
        "A Pydantic model instance should be serialized to pretty-printed JSON.",
        "pydantic_model_input",
    ),
    (
        {"a": 1, "b": [2, 3]},
        "A standard dictionary should be serialized to pretty-printed JSON.",
        "dict_input",
    ),
    (
        {"user": {"name": "test", "id": 1}, "status": "active"},
        "A dictionary (JSON object) with a nested object should be serialized correctly.",
        "json_object_input",
    ),
]


@pytest.mark.parametrize(
    "input_val, description, case", CASES, ids=[c[-1] for c in CASES]
)
def test_to_display_block(
    input_val: Any,
    description: str,
    case: str,
    write_case_markdown: Callable[..., Any],
    append_results: Callable[..., Any],
) -> None:
    """
    Tests that to_display_block correctly formats various input types
    and saves the output to a markdown file for review.
    """
    out = to_display_block(input_val)

    md_file = write_case_markdown(
        renderer="to_display_block",
        case=case,
        input_params={"input": input_val},
        output=out,
        expectation=description,
        review=None,
    )

    append_results(file=md_file, review=None)
