from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from prompt_craft_kit.renderers.render_function import render_function
from prompt_craft_kit.runtime_context import pop_open_tag
from prompt_craft_kit.runtime_context import push_open_tag


@render_function("section_start")
def section_start(tag: str) -> str:
    """
    Emits <tag ...> and pushes `tag` on the open-tag stack.
    """
    push_open_tag(tag)
    return f"<{tag.upper()}>"


@render_function("section_end")
def section_end(tag: str) -> str:
    """
    Emits </tag>. If `tag` is provided, verifies it matches the most recent open tag.
    If omitted, closes the most recent open tag.
    """
    closed = pop_open_tag(tag)
    return f"</{closed.upper()}>"


@contextmanager
def section(tag: str) -> Iterator[None]:
    """
    Context manager that calls section_start(...) on entry and section_end() on exit.
    """
    section_start(tag)
    try:
        yield
    finally:
        section_end(tag)
