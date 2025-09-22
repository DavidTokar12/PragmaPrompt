from __future__ import annotations

import json

from collections.abc import Mapping
from dataclasses import asdict
from dataclasses import is_dataclass
from typing import cast
from typing import overload

from pydantic import BaseModel

from pragma_prompt.renderers.render_function import render_function
from pragma_prompt.renderers.types import DataclassInstance
from pragma_prompt.renderers.types import JsonObj
from pragma_prompt.renderers.types import SupportsModelDump


@overload
def output_format(data: JsonObj | None) -> str: ...
@overload
def output_format(data: BaseModel) -> str: ...
@overload
def output_format(data: DataclassInstance) -> str: ...
@overload
def output_format(data: SupportsModelDump) -> str: ...


@render_function("output_format")
def output_format(
    data: JsonObj | BaseModel | DataclassInstance | SupportsModelDump | None,
) -> str:
    """Render an output format instance as pretty, deterministic JSON.

    Accepts:
      - Mapping[str, JsonValue]
      - dataclass instance
      - Pydantic v2 BaseModel instance
      - object with a ``model_dump()`` method returning a mapping
      - None (renders empty object)
    """

    if data is None:
        payload: object = {}
    elif isinstance(data, BaseModel):
        payload = data.model_dump()
    elif is_dataclass(data) and not isinstance(data, type):
        payload = asdict(data)
    elif isinstance(data, Mapping):
        payload = dict(data)
    elif hasattr(data, "model_dump") and callable(getattr(data, "model_dump")):
        payload = cast(SupportsModelDump, data).model_dump()
    else:
        raise TypeError(
            "output_format expects one of: Mapping[str, JsonValue], a dataclass instance, "
            "a Pydantic v2 BaseModel (or object with model_dump()), or None."
        )

    try:
        return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)
    except TypeError as e:
        raise ValueError("Failed to serialize output format instance to JSON.") from e


@overload
def output_example(
    data: JsonObj | None, *, comments: Mapping[str, str] | None = ...
) -> str: ...
@overload
def output_example(
    data: BaseModel, *, comments: Mapping[str, str] | None = ...
) -> str: ...
@overload
def output_example(
    data: DataclassInstance, *, comments: Mapping[str, str] | None = ...
) -> str: ...
@overload
def output_example(
    data: SupportsModelDump, *, comments: Mapping[str, str] | None = ...
) -> str: ...


@render_function("output_example")
def output_example(
    data: JsonObj | BaseModel | DataclassInstance | SupportsModelDump | None,
    *,
    comments: Mapping[str, str] | None = None,
) -> str:
    """Render an **output example** (pretty JSON) with optional trailing ``//`` comments.

    Every comment key **must** exist in the input object. Missing comments for some
    fields are allowed.

    Args:
        data: Object to normalize (same accepted types as :func:`output_format`).
        comments: Optional mapping of ``field_name -> comment``. Each key must
            exist in the normalized object.

    Returns:
        A JSON-like string with inline ``// comments`` after values.

    Raises:
        TypeError: If ``data`` or ``comments`` has invalid type(s).
        ValueError: If comments refer to unknown keys or a value isn't JSON-serializable.
    """
    # Normalize input
    if data is None:
        payload: object = {}
    elif isinstance(data, BaseModel):
        payload = data.model_dump()
    elif is_dataclass(data) and not isinstance(data, type):
        payload = asdict(data)
    elif isinstance(data, Mapping):
        payload = dict(data)
    elif hasattr(data, "model_dump") and callable(data.model_dump):
        payload = cast("SupportsModelDump", data).model_dump()
    else:
        raise TypeError(
            "output_example expects one of: Mapping[str, JsonValue], a dataclass instance, "
            "a Pydantic v2 BaseModel (or object with model_dump()), or None."
        )

    if not isinstance(payload, Mapping):
        raise TypeError("output_example: normalized input is not a mapping")

    # Validate comments
    if comments is not None:
        if not isinstance(comments, Mapping):
            raise TypeError("output_example.comments must be a Mapping[str, str]")
        keys = [str(k) for k in payload]
        unknown = sorted(set(comments.keys()) - set(keys))
        if unknown:
            raise ValueError(
                "output_example: comments provided for unknown key(s): "
                + ", ".join(unknown)
            )

    # Build pretty JSON with inline comments
    keys_sorted = sorted(payload.keys(), key=lambda k: str(k))

    lines: list[str] = ["{"]
    for i, k in enumerate(keys_sorted):
        v = payload[k]
        try:
            v_json = json.dumps(v, ensure_ascii=False, sort_keys=True, indent=2)
        except TypeError as e:
            raise ValueError(
                f"output_example: failed to serialize value for key '{k}'"
            ) from e

        is_last = i == (len(keys_sorted) - 1)
        comment = (comments or {}).get(str(k)) if comments else None

        if "\n" not in v_json:
            line = f"  {json.dumps(str(k))}: {v_json}"
            if not is_last:
                line += ","
            if comment:
                line += f" // {comment}"
            lines.append(line)
        else:
            v_lines = v_json.splitlines()
            lines.append(f"  {json.dumps(str(k))}: {v_lines[0]}")
            for mid in v_lines[1:-1]:
                lines.append(f"  {mid}")
            tail = "," if not is_last else ""
            if comment:
                tail += f" // {comment}"
            lines.append(f"  {v_lines[-1]}{tail}")

    lines.append("}")
    return "\n".join(lines)
