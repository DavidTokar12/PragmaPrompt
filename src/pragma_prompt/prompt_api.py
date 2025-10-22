from __future__ import annotations

import sys

from collections.abc import Iterator
from pathlib import Path
from typing import Any
from typing import Generic
from typing import TypeVar
from typing import cast
from typing import get_origin
from typing import get_type_hints

from pragma_prompt.exceptions import ConfigurationError
from pragma_prompt.render_engine import render_path
from pragma_prompt.render_engine import render_path_in_current_session
from pragma_prompt.renderers.render_plan import RenderPlan
from pragma_prompt.runtime_context import context as rt_context
from pragma_prompt.runtime_context import is_in_session
from pragma_prompt.runtime_context import join_sections as rt_join
from pragma_prompt.runtime_context import render_model as rt_render_model
from pragma_prompt.runtime_context import render_plan_entries as rt_render_plan


CnsT = TypeVar("CnsT")
CtxT = TypeVar("CtxT")
RM = TypeVar("RM")


class _BaseItem:
    """
    Common descriptor for file-backed items (prompts/components).
    Handles owner/attr/filename/path resolution.
    """

    __slots__ = ("_attr", "_file_path", "_filename", "_last_render_plan", "_owner")

    def __init__(self, filename: str | None = None) -> None:
        self._filename = filename
        self._attr: str | None = None
        self._file_path: Path | None = None
        self._owner: type[_BaseModule[Any]] | None = None
        self._last_render_plan: RenderPlan | None = None

    def _late_init(self, owner: type[_BaseModule[Any]], attr_name: str) -> None:
        """Called by the module's __init_subclass__ to bind this item to its owner."""
        self._owner = owner
        self._attr = attr_name
        self._set_file_name()
        self._set_path()

    def _set_file_name(self) -> None:
        """Determine the final filename, defaulting to the attribute name."""
        if self._filename is None:
            self._filename = f"{self._ensure_attr()}.py"
            return
        if not self._filename.endswith(".py"):
            self._filename = f"{self._filename}.py"

    def _set_path(self) -> None:
        """Resolve the full, absolute path to the item's file."""
        owner = self._ensure_owner()
        filename = self._filename or f"{self._ensure_attr()}.py"
        path = (owner.module_dir_path() / filename).resolve()

        if not path.is_file():
            raise FileNotFoundError(f"Prompt file not found at expected path: {path}")

        self._file_path = path

    def _ensure_owner(self) -> type[_BaseModule[Any]]:
        if self._owner is None:
            raise ConfigurationError("Item has no owner module.")
        return self._owner

    def _ensure_attr(self) -> str:
        if self._attr is None:
            raise ConfigurationError("Item has no attribute name.")
        return self._attr

    def _ensure_path(self) -> Path:
        if self._file_path is None:
            raise ConfigurationError("Item has no file path.")
        return self._file_path

    @property
    def plan(self) -> RenderPlan | None:
        """Get the last render plan, or None if render hasn't been called."""
        return self._last_render_plan


def _is_item_annotation(tp: Any) -> bool:
    origin = get_origin(tp) or tp
    return isinstance(origin, type) and issubclass(origin, _BaseItem)


class _BaseModule(Generic[CnsT]):
    """
    Common module base: validates/normalizes module_dir and binds owned items.
    """

    module_dir: Path | None = None
    constants: CnsT = None  # type: ignore[assignment]
    __module_dir_path: Path | None = None

    @classmethod
    def module_dir_path(cls) -> Path:
        if cls.__module_dir_path is None:
            # This should be unreachable if __init_subclass__ runs correctly.
            raise ConfigurationError(f"{cls.__name__}: module_dir_path not set")
        return cls.__module_dir_path

    def __init_subclass__(cls) -> None:
        # Avoid running this logic on the abstract base classes themselves
        if cls.__name__ in ("PromptModule", "ComponentModule", "_BaseModule"):
            return

        path_source: Path
        if cls.module_dir is not None:
            path_source = Path(cls.module_dir)
        else:
            try:
                module = sys.modules[cls.__module__]
                if not hasattr(module, "__file__") or module.__file__ is None:
                    raise AttributeError
                path_source = Path(module.__file__).parent
            except (KeyError, AttributeError) as e:
                raise ConfigurationError(
                    f"{cls.__name__}: could not automatically determine 'module_dir'. "
                    "Please set it explicitly on t he class."
                ) from e

        resolved_path = path_source.resolve()
        if not resolved_path.is_dir():
            raise ConfigurationError(
                f"{cls.__name__}: resolved module_dir is not a valid directory: {resolved_path}"
            )

        cls.module_dir = resolved_path
        cls.__module_dir_path = resolved_path

        hints = get_type_hints(cls)

        for attr_name, hint in hints.items():
            if not _is_item_annotation(hint):
                continue

            origin = get_origin(hint) or hint
            inst = getattr(cls, attr_name, None)

            if not isinstance(inst, _BaseItem):
                inst = origin()
                setattr(cls, attr_name, inst)

            if getattr(inst, "_owner", None) is None:
                inst._late_init(owner=cls, attr_name=attr_name)

        for attr_name, value in cls.__dict__.items():
            if isinstance(value, _BaseItem):
                value._late_init(owner=cls, attr_name=attr_name)


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

    def __init__(self, filename: str | None = None) -> None:
        super().__init__(filename)

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
        in_session = is_in_session()

        if in_session:
            raise RuntimeError(
                "Rendering prompts inside other prompts is not allowed! Use a component instead."
            )

        prompt_owner = self._ensure_owner()
        path = self._ensure_path()

        result = render_path(
            path,
            constants=getattr(prompt_owner, "constants", None),
            context=context,
            render_model=render_model,
        )
        # Save the render plan JSON for later access
        self._last_render_plan = result.plan
        return result.text


# -------------------------- Components --------------------------


class ComponentModule(_BaseModule[CnsT], Generic[CnsT]):
    """
    Subclass once with your concrete constants type and set:
      - module_dir: Path | str (folder with your component .py files)
      - constants:  CnsT (your constants instance)
    """


class Component(_BaseItem, Generic[RM]):
    """
    Descriptor/handle for a reusable component snippet.
    Components are constants-only snippets; they do not expose prompt context but can
    read the active render model, mirroring prompt files.
    """

    def __init__(self, filename: str | None = None) -> None:
        super().__init__(filename)

    @property
    def render_model(self) -> RM:
        """Access the current render model (if any) while inside a render session."""
        return cast("RM", rt_render_model())

    def render(self, render_model: RM | None = None) -> str:
        """
        If called during an active prompt render, execute the component into the
        current session (appending the component's sections in-order) and return
        just the text that was added by this call.

        If called with no active session, render standalone using module constants
        and an optional ``render_model`` (mirroring prompt rendering), returning the
        full text.
        """
        owner = self._ensure_owner()
        path = self._ensure_path()

        if is_in_session():
            if render_model is not None:
                raise RuntimeError(
                    "Cannot override render_model while inside an active render session."
                )
            before_len = len(rt_render_plan())
            render_path_in_current_session(path)
            # Note: In session mode we can't get the plan since it's part of the parent's plan
            return rt_join(from_index=before_len)

        result = render_path(
            path,
            constants=getattr(owner, "constants", None),
            context=None,
            render_model=render_model,
        )
        self._last_render_plan = result.plan
        return result.text
