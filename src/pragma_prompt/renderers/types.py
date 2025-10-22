from __future__ import annotations

from collections.abc import Mapping
from collections.abc import Sequence
from typing import TYPE_CHECKING
from typing import Any
from typing import Protocol
from typing import TypeAlias

from pydantic import BaseModel


JsonScalar = str | int | float | bool | None
JsonValue: TypeAlias = JsonScalar | Mapping[str, "JsonValue"] | Sequence["JsonValue"]
JsonObj: TypeAlias = Mapping[str, JsonValue]

if TYPE_CHECKING:
    from _typeshed import DataclassInstance as DataclassInstance
else:

    class DataclassInstance:
        pass


class SupportsModelDump(Protocol):
    def model_dump(self, *args: Any, **kwargs: Any) -> JsonObj: ...


BaseResponseLike: TypeAlias = (
    JsonObj | BaseModel | DataclassInstance | str | dict[str, Any]
)
LlmResponseLike: TypeAlias = BaseResponseLike | Sequence["LlmResponseLike"]
