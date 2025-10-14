from __future__ import annotations

import pytest

import pragma_prompt as pp

from pragma_prompt.runtime_context import session


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
        out = pp.output_example(data, comments=comments)

    assert out == expected


def test_output_example_unknown_comment_key_raises_value_error() -> None:
    data = {"title": "", "body_markdown": "", "flair": ""}
    comments = {"nonexistent": "should raise"}

    with session(), pytest.raises(ValueError):
        pp.output_example(data, comments=comments)


def test_output_example_no_comments() -> None:
    data = {"b": 2, "a": 1}

    expected = "{\n" '  "a": 1,\n' '  "b": 2\n' "}"

    with session():
        out = pp.output_example(data)
    assert out == expected


def test_output_example_root_comment_string() -> None:
    data = {"a": 1}
    expected = '{\n  "a": 1\n} // Overall guidance'
    with session():
        out = pp.output_example(data, comments="Overall guidance")
    assert out == expected


def test_output_example_object_node_comment() -> None:
    """A comment on the whole nested object (no specific subkey)."""
    data = {"user": {"name": "Ada", "age": 30}, "count": 1}
    comments = {"user": "User-level note"}

    expected = (
        "{\n"
        '  "count": 1,\n'
        '  "user": {\n'
        '    "age": 30,\n'
        '    "name": "Ada"\n'
        "  } // User-level note\n"
        "}"
    )

    with session():
        out = pp.output_example(data, comments=comments)
    assert out == expected


def test_output_example_nested_object_comment() -> None:
    data = {"user": {"name": "Ada", "age": 30}, "count": 1}
    comments = {"user": {"name": "Display name"}}

    expected = (
        "{\n"
        '  "count": 1,\n'
        '  "user": {\n'
        '    "age": 30,\n'
        '    "name": "Ada" // Display name\n'
        "  }\n"
        "}"
    )

    with session():
        out = pp.output_example(data, comments=comments)
    assert out == expected


def test_output_example_array_index_comment() -> None:
    data = {"items": [{"id": 1}, {"id": 2}]}
    comments = {"items": {"1": {"id": "second item id"}}}

    expected = (
        "{\n"
        '  "items": [\n'
        "    {\n"
        '      "id": 1\n'
        "    },\n"
        "    {\n"
        '      "id": 2 // second item id\n'
        "    }\n"
        "  ]\n"
        "}"
    )
    with session():
        out = pp.output_example(data, comments=comments)
    assert out == expected


def test_output_example_multiple_nested_comments() -> None:
    data = {"user": {"name": "Ada", "roles": ["admin", "ops"]}, "count": 2}
    comments = {
        "user": {
            "name": "Display name",
            "roles": {"0": "Primary role"},
        },
        "count": "Number of items",
    }

    expected = (
        "{\n"
        '  "count": 2, // Number of items\n'
        '  "user": {\n'
        '    "name": "Ada", // Display name\n'
        '    "roles": [\n'
        '      "admin", // Primary role\n'
        '      "ops"\n'
        "    ]\n"
        "  }\n"
        "}"
    )

    with session():
        out = pp.output_example(data, comments=comments)
    assert out == expected


def test_output_example_path_descends_into_primitive_raises_value_error() -> None:
    data = {"title": "x"}
    # "title" is a primitive; you can't descend further to "x"
    comments = {"title": {"x": "nope"}}
    with session(), pytest.raises(ValueError):
        pp.output_example(data, comments=comments)


def test_output_example_array_index_out_of_range_raises_value_error() -> None:
    data = {"items": [{"id": 1}]}
    comments = {"items": {"5": {"id": "oob"}}}
    with session(), pytest.raises(ValueError):
        pp.output_example(data, comments=comments)


def test_output_example_array_index_not_numeric_raises_value_error() -> None:
    data = {"items": [{"id": 1}]}
    comments = {"items": {"first": {"id": "must be numeric string"}}}
    with session(), pytest.raises(ValueError):
        pp.output_example(data, comments=comments)


def test_output_example_non_serializable_value_raises_value_error() -> None:
    # sets are not JSON-serializable
    data = {"tags": {"a", "b"}}
    with session(), pytest.raises(ValueError):
        pp.output_example(data)


def test_output_example_does_not_mutate_inputs() -> None:
    data = {"a": {"b": 1}}
    comments = {"a": {"b": "note"}}
    with session():
        _ = pp.output_example(data, comments=comments)
    assert data == {"a": {"b": 1}}
    assert comments == {"a": {"b": "note"}}
