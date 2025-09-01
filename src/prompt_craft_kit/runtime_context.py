from __future__ import annotations

import contextlib
import contextvars

from collections.abc import Iterable
from collections.abc import Iterator
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any
from typing import Generic
from typing import TypeVar

from prompt_craft_kit.exceptions import LoaderError
from prompt_craft_kit.renderers.prompt_section import PromptSection


CnsT = TypeVar("CnsT")
CtxT = TypeVar("CtxT")
RmT = TypeVar("RmT")


@dataclass
class _State(Generic[CnsT, CtxT, RmT]):
    """
    Internal per-render state:
      - sections: collected prompt sections in order
      - constants: module-level constants instance
      - context:   per-render context instance
      - render_model: per-file render model (None for components)
    """

    sections: list[PromptSection] = field(default_factory=list)
    exec_stack: list[Path] = field(default_factory=list)
    open_tags: list[str] = field(default_factory=list)

    constants: CnsT | None = None
    context: CtxT | None = None
    render_model: RmT | None = None


_VAR: contextvars.ContextVar[_State[Any, Any, Any] | None] = contextvars.ContextVar(
    "pck_runtime", default=None
)


def begin(
    *,
    constants: CnsT | None = None,
    context: CtxT | None = None,
    render_model: RmT | None = None,
) -> contextvars.Token[_State[Any, Any, Any] | None]:
    """
    Start a render session. Returns a token you must pass to end().
    """
    state: _State[CnsT, CtxT, RmT] = _State(
        sections=[],
        constants=constants,
        context=context,
        render_model=render_model,
    )
    return _VAR.set(state)


def end(token: contextvars.Token[_State[Any, Any, Any] | None]) -> None:
    """
    End a render session and clear the ContextVar.
    Refuses to close if there are pending includes or unclosed section tags.
    """
    s = _VAR.get()
    errors: list[str] = []

    if s is not None:
        if s.exec_stack:
            chain = " -> ".join(p.name for p in s.exec_stack)
            errors.append(f"pending include stack: {chain}")
        if s.open_tags:
            tagtrail = " > ".join(s.open_tags)
            errors.append(f"{len(s.open_tags)} unclosed section tag(s): {tagtrail}")

    try:
        _VAR.reset(token)
    except Exception as e:
        raise RuntimeError(
            f"prompt_craft_kit: failed to clear render context: {e}"
        ) from e

    if errors:
        raise LoaderError("render session ended uncleanly: " + "; ".join(errors))


@contextlib.contextmanager
def session(
    *,
    constants: CnsT | None = None,
    context: CtxT | None = None,
    render_model: RmT | None = None,
) -> Iterator[None]:
    token = begin(constants=constants, context=context, render_model=render_model)
    try:
        yield
    finally:
        end(token)


def _state() -> _State[Any, Any, Any]:
    s = _VAR.get()
    if s is None:
        raise RuntimeError(
            "prompt_craft_kit: accessed render state outside of an active render"
        )
    return s


# -------- simple (untyped) accessors; useful internally --------


def constants() -> Any:
    return _state().constants


def context() -> Any:
    return _state().context


def render_model() -> Any | None:
    return _state().render_model


# -------- sections API (unchanged) --------


def add_section(section: PromptSection) -> None:
    _state().sections.append(section)


def extend_sections(sections: Iterable[PromptSection]) -> None:
    _state().sections.extend(sections)


def sections() -> list[PromptSection]:
    return list(_state().sections)


def join(sep: str = "\n") -> str:
    return sep.join(sec.body for sec in _state().sections)


# -------- execution stack (for cycle detection) --------


@contextlib.contextmanager
def exec_stack_guard(path: Path) -> Iterator[None]:
    """
    Guard execution of a prompt/component file within the current session.

    - Circular include detection (if `path` already on the stack).
    - LIFO discipline for the include stack.
    - Tag-leak detection: the file must not change the number of open tags.
    """
    s = _state()

    if path in s.exec_stack:
        chain = " -> ".join(p.name for p in [*s.exec_stack, path])
        raise LoaderError(
            f"Circular include detected while executing '{path.name}': {chain}"
        )

    tag_depth_before = len(s.open_tags)

    s.exec_stack.append(path)
    try:
        yield
    finally:
        if not s.exec_stack:
            raise RuntimeError(
                "exec_stack_guard: unbalanced stack (empty on pop); this is a bug."
            )
        top = s.exec_stack[-1]
        if top != path:
            raise RuntimeError(
                f"exec_stack_guard: LIFO violation; tried to pop '{path.name}' "
                f"but top is '{top.name}'. This is a bug."
            )
        s.exec_stack.pop()

        tag_depth_after = len(s.open_tags)
        if tag_depth_after != tag_depth_before:
            leaked = s.open_tags[tag_depth_before:]
            leaked_list = ", ".join(leaked) if leaked else "(unknown)"
            raise LoaderError(
                f"File '{path.name}' left {abs(tag_depth_after - tag_depth_before)} "
                f"unclosed section tag(s): {leaked_list}"
            )


def push_open_tag(tag: str) -> None:
    _state().open_tags.append(tag)


def pop_open_tag(expected: str | None = None) -> str:
    s = _state().open_tags
    if not s:
        raise RuntimeError("section_end(): no open section to close")
    tag = s.pop()
    if expected is not None and expected != tag:
        raise RuntimeError(
            f"section_end(): mismatched tag: tried to close '{expected}', "
            f"but last open is '{tag}'"
        )
    return tag
