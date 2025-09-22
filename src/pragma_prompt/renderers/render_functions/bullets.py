from __future__ import annotations

from collections.abc import Mapping
from collections.abc import Sequence
from typing import Any
from typing import overload

from pragma_prompt.renderers.render_function import render_function
from pragma_prompt.renderers.utils import to_display_block


@overload
def bullets(items: Mapping[str, Any]) -> str: ...
@overload
def bullets(items: Sequence[tuple[str, Any]]) -> str: ...
@overload
def bullets(items: Sequence[Any]) -> str: ...


@render_function("bullets")
def bullets(
    items: Mapping[str, Any] | Sequence[tuple[str, Any]] | Sequence[Any],
) -> str:
    """Render a compact bullet list.

    Accepts either:
      * a mapping (rendered as "- key: value"),
      * a sequence of (key, value) tuples, or
      * a plain sequence of values (rendered as "- value").

    Notes:
        Strings are **not** treated as sequences of characters. If a single
        string is passed, it is rendered as one bullet entry.

    Examples:
        >>> bullets({"role": "analyst", "tone": "concise"})
        '- role: analyst\\n- tone: concise'

        >>> bullets([("role", "analyst"), ("tone", "concise")])
        '- role: analyst\\n- tone: concise'

        >>> bullets(["Discussion", "Serious", "Debate"])
        '- Discussion\\n- Serious\\n- Debate'

    Returns:
        A newline-joined string of bullet items.
    """
    # Mapping -> key/value pairs
    if isinstance(items, Mapping):
        pairs: Sequence[tuple[Any, Any]] = list(items.items())
        lines = [f"- {k}: {to_display_block(v)}" for k, v in pairs]
        return "\n".join(lines)

    # Guard: don't iterate characters of a string/bytes
    if isinstance(items, str | bytes):
        s = items.decode("utf-8", "replace") if isinstance(items, bytes) else items
        return f"- {to_display_block(s)}"

    seq: Sequence[Any] = list(items)
    out_lines: list[str] = []
    for el in seq:
        if isinstance(el, tuple) and len(el) == 2:
            k, v = el
            out_lines.append(f"- {k}: {to_display_block(v)}")
        else:
            out_lines.append(f"- {to_display_block(el)}")
    return "\n".join(out_lines)
