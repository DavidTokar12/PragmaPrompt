from __future__ import annotations

import json

from collections.abc import Mapping
from dataclasses import asdict
from dataclasses import is_dataclass
from typing import Any

from pydantic import BaseModel

from pragma_prompt.renderers.types import LlmResponseLike


def _to_plain_obj(x: Any) -> Any:
    """
    Recursively normalize an object to a plain Python object suitable for
    JSON serialization. Handles nested Pydantic models, dataclasses, lists, and dicts.
    """
    if isinstance(x, BaseModel):
        return x.model_dump()
    if is_dataclass(x) and not isinstance(x, type):
        return asdict(x)
    if isinstance(x, list | tuple):
        return [_to_plain_obj(item) for item in x]
    if isinstance(x, Mapping):
        return {k: _to_plain_obj(v) for k, v in x.items()}
    # Fallback for primitives (str, int, float, bool, None)
    return x


def format_json(obj: LlmResponseLike) -> str:
    """
    Consistently formats a Python object as a pretty-printed JSON string,
    preserving key order. Handles Pydantic models and dataclasses.
    """
    plain_obj = _to_plain_obj(obj)
    return json.dumps(plain_obj, indent=2, ensure_ascii=False)


def to_display_block(x: LlmResponseLike) -> str:
    """
    For rendering inside prompt text:
      - strings that are valid JSON are pretty-printed;
      - strings that are not valid JSON are returned as-is;
      - everything else is pretty-printed as JSON.
    """
    if isinstance(x, str):
        try:
            parsed = json.loads(x)
            return format_json(parsed)
        except json.JSONDecodeError:
            return x

    return format_json(x)
