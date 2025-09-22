from __future__ import annotations

from collections.abc import Callable
from collections.abc import Mapping
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel


Serializable = Any


def _qualname(func: Callable[..., Any]) -> str:
    module = getattr(func, "__module__", "")
    qualname = getattr(func, "__qualname__", getattr(func, "__name__", repr(func)))
    return f"{module}.{qualname}" if module else qualname


def _normalize(value: Any) -> Serializable:
    """Best-effort conversion of values into JSON-serialisable data."""
    if isinstance(value, str | int | float | bool) or value is None:
        return value
    if isinstance(value, bytes):
        try:
            return value.decode("utf-8")
        except Exception:
            return repr(value)
    if isinstance(value, list | tuple | set):
        return [_normalize(v) for v in value]
    if isinstance(value, Mapping):
        return {str(k): _normalize(v) for k, v in value.items()}
    if hasattr(value, "__dict__"):
        try:
            return {
                "__class__": f"{value.__class__.__module__}.{value.__class__.__name__}",
                **{k: _normalize(v) for k, v in vars(value).items()},
            }
        except Exception:
            return repr(value)
    return repr(value)


@dataclass(slots=True)
class RenderCall:
    """Snapshot of a renderer invocation captured during a prompt render."""

    renderer: str
    callable_path: str
    args: tuple[Serializable, ...]
    kwargs: dict[str, Serializable]
    result: str

    def to_json_dict(self) -> dict[str, Serializable]:
        return {
            "renderer": self.renderer,
            "callable": self.callable_path,
            "args": list(self.args),
            "kwargs": self.kwargs,
            "result": self.result,
        }


def build_render_call(
    *,
    renderer: str,
    func: Callable[..., str],
    args: Sequence[Any],
    kwargs: Mapping[str, Any],
    result: str,
) -> RenderCall:
    snapshot_args = tuple(_normalize(a) for a in args)
    snapshot_kwargs = {k: _normalize(v) for k, v in kwargs.items()}
    return RenderCall(
        renderer=renderer,
        callable_path=_qualname(func),
        args=snapshot_args,
        kwargs=snapshot_kwargs,
        result=result,
    )


class RenderPlan(BaseModel):
    """A pydantic model containing a list of render calls from a prompt execution."""

    calls: list[RenderCall]

    def to_text(self, *, sep: str = "\n", from_index: int = 0) -> str:
        """Convert the render plan to text output."""
        if from_index < 0:
            raise ValueError("from_index must be >= 0")
        parts = [call.result for call in self.calls[from_index:]]
        return sep.join(parts)


@dataclass(slots=True)
class RenderResult:
    _plan: list[RenderCall]

    @property
    def plan(self) -> RenderPlan:
        """Get the render plan as a pydantic model."""
        return RenderPlan(calls=self._plan)

    @property
    def text(self) -> str:
        """Get the rendered text from the plan."""
        return self.plan.to_text()
