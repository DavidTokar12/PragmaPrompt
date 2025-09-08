from __future__ import annotations

import pytest

import prompt_craft_kit as pck
from prompt_craft_kit.runtime_context import session


def test_output_example_renders_with_comments_subset() -> None:
    data = {"title": "", "body_markdown": "", "flair": ""}
    comments = {
        "body_markdown": "Main content in Markdown",
        "flair": "Choose from allowed list",
    }

    expected = (
        "{\n"
        '  "body_markdown": "", // Main content in Markdown\n'
        '  "flair": "", // Choose from allowed list\n'
        '  "title": ""\n'
        "}"
    )

    with session():
        out = pck.output_example(data, comments=comments)

    assert out == expected


def test_output_example_unknown_comment_key_raises_value_error() -> None:
    data = {"title": "", "body_markdown": "", "flair": ""}
    comments = {"nonexistent": "should raise"}

    with session():
        with pytest.raises(ValueError):
            pck.output_example(data, comments=comments)
