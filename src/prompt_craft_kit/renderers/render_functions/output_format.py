from __future__ import annotations

import json

from collections.abc import Mapping
from dataclasses import asdict
from dataclasses import is_dataclass
from typing import Protocol
from typing import overload

from pydantic import BaseModel

from prompt_craft_kit.renderers.render_function import render_function
from prompt_craft_kit.renderers.renderers import Renderers


class DataclassInstance(Protocol):
    __dataclass_fields__: Mapping[str, object]


JsonObj = Mapping[str, object]


@overload
def output_format(data: JsonObj) -> str: ...
@overload
def output_format(data: BaseModel) -> str: ...
@overload
def output_format(data: DataclassInstance) -> str: ...


@render_function(Renderers.OUTPUT_FORMAT)
def output_format(
    data: JsonObj | BaseModel | DataclassInstance,
) -> str:
    """
    Render an output format instance as pretty JSON.

    Accepts:
      - Mapping[str, object]
      - dataclass instance
      - Pydantic v2 BaseModel instance
      - None (renders empty object)
    """

    if data is None:
        payload: object = {}
    elif isinstance(data, BaseModel):
        payload = data.model_dump()
    elif is_dataclass(data):
        payload = asdict(data)
    elif isinstance(data, Mapping):
        payload = dict(data)
    else:
        raise TypeError(
            "output_format expects a Mapping[str, object], a dataclass instance, "
            "a Pydantic v2 BaseModel instance, or None."
        )

    try:
        return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)
    except TypeError as e:
        raise ValueError("Failed to serialize output format instance to JSON.") from e
