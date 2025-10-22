from __future__ import annotations

import json

from collections.abc import Mapping
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import is_dataclass
from typing import Any
from typing import TypeAlias
from typing import cast

from pydantic import BaseModel

from pragma_prompt.renderers.render_function import render_function
from pragma_prompt.renderers.types import LlmResponseLike


# ============================================================
# Comments: recursively nested Mapping[str, str | Mapping]
#   - Each object node EITHER has a single string comment OR per-subkey comments (mapping), not both.
#   - Leaf is always a string (the comment text).
#   - Keys are strings; arrays use numeric string indices: "0", "1", ...
#   - The top-level `comments` may also be a single string (root comment).
# ============================================================

CommentTreeOrStr: TypeAlias = str | Mapping[str, "CommentTreeOrStr"]
CommentTree: TypeAlias = Mapping[str, CommentTreeOrStr]


# ============================================================
# Rendering nodes
# ============================================================


@dataclass
class Node:
    comment: str | None = None

    def render(self, indent: int = 0) -> list[str]:
        raise NotImplementedError


def _with_comma_before_comment(s: str) -> str:
    # If the line already ends with a comma, leave it.
    if s.endswith(","):
        return s
    # If there's an inline comment, insert the comma right before it.
    anchor = " // "
    i = s.find(anchor)
    if i != -1:
        return s[:i] + "," + s[i:]
    # Otherwise, just add a trailing comma.
    return s + ","


@dataclass
class PrimitiveNode(Node):
    value: Any = None

    def render(self, indent: int = 0) -> list[str]:
        pad = " " * indent
        try:
            body = json.dumps(self.value, ensure_ascii=False, sort_keys=True)
        except TypeError as e:
            raise ValueError("output_example: failed to serialize value") from e
        if self.comment:
            body += f" // {self.comment}"
        return [pad + body]


@dataclass
class ObjectNode(Node):
    children: list[tuple[str, Node]] | None = None

    def render(self, indent: int = 0) -> list[str]:
        pad = " " * indent
        lines: list[str] = [pad + "{"]
        items = self.children or []
        n = len(items)
        for i, (k, child) in enumerate(items):
            child_lines = child.render(indent + 2)
            is_last = i == n - 1

            if len(child_lines) == 1:
                # Single-line child → add comma BEFORE any inline comment if not last
                line = f"{pad}  {json.dumps(str(k))}: {child_lines[0].lstrip()}"
                if not is_last:
                    line = _with_comma_before_comment(line)
                lines.append(line)
            else:
                # Multi-line child → for the last line, insert comma BEFORE comment if not last
                first = child_lines[0].lstrip()
                lines.append(f"{pad}  {json.dumps(str(k))}: {first}")
                for mid in child_lines[1:-1]:
                    lines.append(mid)
                last_line = child_lines[-1]
                if not is_last:
                    last_line = _with_comma_before_comment(last_line)
                lines.append(last_line)

        closing = pad + "}"
        if self.comment:
            closing += f" // {self.comment}"
        lines.append(closing)
        return lines


@dataclass
class ArrayNode(Node):
    items: list[Node] | None = None

    def render(self, indent: int = 0) -> list[str]:
        pad = " " * indent
        lines: list[str] = [pad + "["]
        elems = self.items or []
        n = len(elems)
        for i, item in enumerate(elems):
            child_lines = item.render(indent + 2)
            is_last = i == n - 1

            if len(child_lines) == 1:
                # Single-line element → add comma BEFORE any inline comment if not last
                line = pad + "  " + child_lines[0].lstrip()
                if not is_last:
                    line = _with_comma_before_comment(line)
                lines.append(line)
            else:
                # Multi-line element → adjust the last line
                lines.extend(child_lines[:-1])
                last_line = child_lines[-1]
                if not is_last:
                    last_line = _with_comma_before_comment(last_line)
                lines.append(last_line)

        closing = pad + "]"
        if self.comment:
            closing += f" // {self.comment}"
        lines.append(closing)
        return lines


# ============================================================
# Normalization helpers
# ============================================================


def _normalize_payload(data: Any) -> Any:
    if data is None:
        return {}
    if isinstance(data, BaseModel):
        return data.model_dump()
    if is_dataclass(data) and not isinstance(data, type):
        return asdict(data)
    if isinstance(data, Mapping):
        return dict(data)
    if hasattr(data, "model_dump") and callable(data.model_dump):
        return cast("Any", data).model_dump()
    return data  # list or primitive


# ============================================================
# Comment validation / build rules
#   - For a given object/array node:
#       * comments can be a string (node-level) OR a mapping of subkeys (not both)
#       * subkey mapping keys must exist (objects) / be valid indices (arrays)
# ============================================================


def _build_node(
    value: Any,
    comments: CommentTreeOrStr | None,
) -> Node:
    # PRIMITIVE ------------------------------------------------
    if not isinstance(value, Mapping) and not isinstance(value, list):
        if isinstance(comments, Mapping):
            # Trying to descend into a primitive
            raise ValueError("output_example: path descends into a primitive value")
        if isinstance(comments, str):
            return PrimitiveNode(comment=comments, value=value)
        return PrimitiveNode(value=value)

    # OBJECT ---------------------------------------------------
    if isinstance(value, Mapping):
        keys_sorted = sorted(value.keys(), key=lambda k: str(k))

        if isinstance(comments, str):
            # Node-level comment; children get no additional comments
            children = [(str(k), _build_node(value[k], None)) for k in keys_sorted]
            return ObjectNode(comment=comments, children=children)

        # comments is None or Mapping
        if comments is not None and not isinstance(comments, Mapping):
            raise TypeError(
                "output_example: object comments must be a string or a mapping"
            )

        # Validate: if mapping provided, all comment keys must exist in object
        if isinstance(comments, Mapping):
            for ck in comments:
                if ck not in value:
                    raise ValueError(
                        f"output_example: comments provided for unknown key: '{ck}'"
                    )

        children: list[tuple[str, Node]] = []  # type: ignore[no-redef]
        for k in keys_sorted:
            sub_c = comments.get(str(k)) if isinstance(comments, Mapping) else None
            # sub_c may be a string (node-level comment for the child) or a mapping (per-subkey)
            if isinstance(sub_c, Mapping | str) or sub_c is None:
                child = _build_node(value[k], sub_c)
            else:
                raise TypeError(
                    "output_example: invalid comment shape; leaf must be a string or mapping"
                )
            children.append((str(k), child))

        return ObjectNode(comment=None, children=children)

    assert isinstance(value, list)

    if isinstance(comments, str):
        items = [_build_node(el, None) for el in value]
        return ArrayNode(comment=comments, items=items)

    if comments is not None and not isinstance(comments, Mapping):
        raise TypeError("output_example: array comments must be a string or a mapping")

    if isinstance(comments, Mapping):
        for ck in comments:
            try:
                idx = int(ck)
            except ValueError as e:
                raise ValueError(
                    f"output_example: expected numeric index at '{ck}'"
                ) from e
            if idx < 0 or idx >= len(value):
                raise ValueError(f"output_example: array index out of range at '{ck}'")

    items: list[Node] = []  # type: ignore[no-redef]
    for idx, el in enumerate(value):
        sub_c = comments.get(str(idx)) if isinstance(comments, Mapping) else None
        if isinstance(sub_c, Mapping | str) or sub_c is None:
            child = _build_node(el, sub_c)
        else:
            raise TypeError(
                "output_example: invalid comment shape under array index; leaf must be a string or mapping"
            )
        items.append(child)

    return ArrayNode(comment=None, items=items)


# ============================================================
# Public renderer
# ============================================================


@render_function("output_example")
def output_example(
    data: LlmResponseLike,
    comments: CommentTreeOrStr | None = None,
) -> str:
    """
    Render pretty, deterministic JSON with optional inline // comments.

    `comments` may be:
      • a root string (comment on the whole value), or
      • a nested mapping[str, str | mapping] that mirrors the shape of `data`.

    Rules per node:
      • For any object/array node, EITHER provide a single string (node-level comment)
        OR provide a mapping of subkeys (per-field/per-index comments), not both.
      • Object comment keys must exist. Array comment keys must be numeric strings within range.

    Behavior:
      • Primitives: comment appended to the same line.
      • Objects/Arrays: comment appended to the closing brace/bracket line.
      • Keys are rendered in sorted order. Output contains valid JSON commas.
    """
    payload = _normalize_payload(data)

    try:
        json.dumps(payload, ensure_ascii=False, sort_keys=True)
    except TypeError as e:
        raise ValueError("output_example: failed to serialize top-level value") from e

    node = _build_node(payload, comments)

    return "\n".join(node.render(indent=0))
