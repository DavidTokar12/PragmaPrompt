from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any
from typing import Generic
from typing import TypeVar
from typing import cast

from prompt_craft_kit.exceptions import ConfigurationError
from prompt_craft_kit.render_engine import render_path
from prompt_craft_kit.render_engine import render_path_in_current_session
from prompt_craft_kit.runtime_context import context as rt_context
from prompt_craft_kit.runtime_context import render_model as rt_render_model
from prompt_craft_kit.runtime_context import sections as rt_sections


CnsT = TypeVar("CnsT")
CtxT = TypeVar("CtxT")
RM = TypeVar("RM")


# -------------------------- Shared base --------------------------


class _BaseModule(Generic[CnsT]):
    """
    Common module base: validates/normalizes module_dir and binds owned items.
    """

    module_dir: Path | str
    constants: CnsT = None  # type: ignore[assignment]

    __module_dir_path: Path | None = None

    @classmethod
    def module_dir_path(cls) -> Path:

        if cls.__module_dir_path is None:
            raise ConfigurationError(f"{cls.__name__}: module_dir_path not set")

        return Path(cls.__module_dir_path)

    def __init_subclass__(cls) -> None:

        if cls.__name__ == "PromptModule" or cls.__name__ == "ComponentModule":
            return

        if not hasattr(cls, "module_dir"):
            raise ConfigurationError(f"{cls.__name__}: missing 'module_dir' Path")

        if not isinstance(cls.module_dir, Path | str):
            raise ConfigurationError(
                f"{cls.__name__}: 'module_dir' must be pathlib.Path or str"
            )

        if isinstance(cls.module_dir, str):
            cls.module_dir = Path(cls.module_dir).resolve()

        cls.__module_dir_path = cls.module_dir

        if not cls.module_dir.is_dir() or not cls.module_dir.exists():
            raise ConfigurationError(
                f"{cls.__name__}: module_dir does not exist or is not a directory: {cls.module_dir}"
            )

        for attr_name, attr_value in cls.__dict__.items():
            if isinstance(attr_value, _BaseItem):
                attr_value._late_init(owner=cls, attr_name=attr_name)


class _BaseItem:
    """
    Common descriptor for file-backed items (prompts/components).
    Handles owner/attr/filename/path resolution.
    """

    __slots__ = ("_attr", "_file_path", "_filename", "_owner")

    def __init__(self, filename: str | None = None) -> None:
        self._filename = filename
        self._attr: str | None = None
        self._file_path: Path | None = None
        self._owner: type[_BaseModule[Any]] | None = None

    # Bound from module __init_subclass__
    def _late_init(self, owner: type[_BaseModule[Any]], attr_name: str) -> None:
        self._owner = owner
        self._attr = attr_name
        self._set_file_name()
        self._set_path()

    def _set_file_name(self) -> None:

        if self._filename is None:
            self._filename = f"{self._ensure_attr()}.py"
            return

        if not self._filename.endswith(".py"):
            self._filename = f"{self._filename}.py"
            return

    def _set_path(self) -> None:
        _owner = self._ensure_owner()
        filename = self._filename or f"{self._ensure_attr()}.py"

        _path = (_owner.module_dir_path() / filename).resolve()

        if not _path.exists() or not _path.is_file():
            raise FileNotFoundError(f"Prompt file not found: {_path}")

        self._file_path = _path

    def _ensure_owner(self) -> type[_BaseModule[Any]]:
        if self._owner is None:
            raise ConfigurationError(
                "Item has no owner module; use a module-bound alias or pass owner=..."
            )
        return self._owner

    def _ensure_attr(self) -> str:
        if self._attr is None:
            raise ConfigurationError(
                "Item has no attribute name; use a module-bound alias or pass attr_name=..."
            )
        return self._attr

    def _ensure_path(self) -> Path:
        if self._file_path is None:
            raise ConfigurationError(
                "Item has no file path; use a module-bound alias or pass owner=... and attr_name=..."
            )
        return self._file_path


# -------------------------- Prompts --------------------------


class PromptModule(_BaseModule[CnsT], Generic[CnsT]):
    """
    Subclass once with your concrete constants type and set:
      - module_dir: Path | str (folder with your prompt .py files)
      - constants:  CnsT (your constants instance)
    """


class Prompt(_BaseItem, Generic[CtxT, RM]):
    """
    Descriptor/handle for a single prompt.

    Access pattern:
      During prompt writing:
        context, render_model = Module.some_prompt
      During prompt rendering:
        text = Module.some_prompt.render(context=..., render_model=...)
    """

    @property
    def context(self) -> CtxT:
        return cast("CtxT", rt_context())

    @property
    def render_model(self) -> RM:
        return cast("RM", rt_render_model())

    def __iter__(self) -> Iterator[object]:
        yield self.context
        yield self.render_model

    def render(
        self, *, context: CtxT | None = None, render_model: RM | None = None
    ) -> str:
        owner = self._ensure_owner()
        path = self._ensure_path()

        return render_path(
            path,
            constants=getattr(owner, "constants", None),
            context=context,
            render_model=render_model,
        )


# -------------------------- Components --------------------------


class ComponentModule(_BaseModule[CnsT], Generic[CnsT]):
    """
    Subclass once with your concrete constants type and set:
      - module_dir: Path | str (folder with your component .py files)
      - constants:  CnsT (your constants instance)
    """


class Component(_BaseItem):
    """
    Descriptor/handle for a reusable component snippet.
    Components are constants-only snippets; they do not expose context or render_model.
    """

    def render(self) -> str:
        """
        If called during an active prompt render, execute the component into the
        current session (appending the component's sections in-order) and return
        just the text that was added by this call.

        If called with no active session, render standalone using only module
        constants and return the full text.
        """
        owner = self._ensure_owner()
        path = self._ensure_path()

        # Try executing into an active session (append sections in-place).
        # If no active session, render standalone.
        try:
            before = rt_sections()
            render_path_in_current_session(path)
            after = rt_sections()
            # Compute only the newly-added section bodies
            idx = len(before)
            return "\n".join(sec.body for sec in after[idx:])
        except RuntimeError:
            # No active session; run standalone with constants-only
            return render_path(
                path,
                constants=getattr(owner, "constants", None),
                context=None,
                render_model=None,
            )
