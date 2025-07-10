"""Prompt template loading and rendering system."""

from __future__ import annotations

import logging

from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any

from jinja2 import BaseLoader
from jinja2 import Environment
from jinja2 import StrictUndefined
from jinja2 import Template
from jinja2 import TemplateNotFound

from prompt_craft_kit.exceptions import LoaderError
from prompt_craft_kit.file_type import FileType
from prompt_craft_kit.prompt_helpers import chain_of_thought
from prompt_craft_kit.prompt_helpers import few_shot
from prompt_craft_kit.prompt_helpers import react_step
from prompt_craft_kit.static_loader import static_loader
from prompt_craft_kit.wrapper_styles import WrapperStyle
from prompt_craft_kit.wrapper_styles import apply_wrapper


if TYPE_CHECKING:
    from collections.abc import Callable

logger = logging.getLogger(__name__)


class ComponentLoader(BaseLoader):
    """Custom Jinja2 loader for component templates with wrapper support."""

    def __init__(
        self, component_loaders: list[type], wrapper_style: WrapperStyle
    ) -> None:
        """Initialize the component loader.

        Args:
            component_loaders: List of classes with static component attributes
            wrapper_style: Style to use when wrapping component content
        """
        self.loaders = component_loaders
        self.loader_map = {loader.__name__: loader for loader in component_loaders}
        self.wrapper_style = wrapper_style

    def get_source(
        self, environment: Environment, template: str
    ) -> tuple[str, str | None, Callable[[], bool]]:
        """Load and wrap component source code.

        Args:
            environment: The Jinja2 environment
            template: Template name to load (can be namespaced with "LoaderName.component")

        Returns:
            Tuple of (source, filename, uptodate_func)

        Raises:
            TemplateNotFound: If template cannot be found
            LoaderError: If template name is ambiguous
        """
        source = self._resolve_component_source(template)
        wrapped_source = self._apply_wrapper(source, template)
        return wrapped_source, None, lambda: True

    def _resolve_component_source(self, template: str) -> str:
        """Resolve component source from template name."""
        if "." in template:
            return self._resolve_namespaced_component(template)
        else:
            return self._resolve_component_by_name(template)

    def _resolve_namespaced_component(self, template: str) -> str:
        """Resolve component using namespace (LoaderName.component)."""
        loader_name, component_name = template.split(".", 1)

        if loader_name not in self.loader_map:
            raise TemplateNotFound(
                f"Component loader namespace '{loader_name}' not found"
            )

        loader = self.loader_map[loader_name]

        if not hasattr(loader, component_name):
            raise TemplateNotFound(
                f"Component '{component_name}' not found in loader '{loader_name}'"
            )

        return getattr(loader, component_name)

    def _resolve_component_by_name(self, component_name: str) -> str:
        """Resolve component by searching all loaders."""
        found_loaders = [
            loader for loader in self.loaders if hasattr(loader, component_name)
        ]

        if not found_loaders:
            raise TemplateNotFound(
                f"Component '{component_name}' not found in any loader"
            )

        if len(found_loaders) > 1:
            loader_names = [loader.__name__ for loader in found_loaders]
            raise LoaderError(
                f"Ambiguous component '{component_name}'. "
                f"Found in multiple loaders: {loader_names}"
            )

        return getattr(found_loaders[0], component_name)

    def _apply_wrapper(self, source: str, component_name: str) -> str:
        """Apply wrapper style to component content."""
        # Extract component name from namespaced template
        if "." in component_name:
            component_name = component_name.split(".", 1)[1]

        return apply_wrapper(source, component_name, self.wrapper_style)


class PromptTemplate:
    """A compiled prompt template that can be rendered with context data.

    This class wraps a Jinja2 template and provides caching and validation
    for prompt rendering operations.
    """

    def __init__(
        self,
        template_name: str,
        jinja_template: Template,
        lazy_render: bool,
        render_model: type | None = None,
    ) -> None:
        """Initialize a prompt template.

        Args:
            template_name: Name of the template file
            jinja_template: Compiled Jinja2 template
            lazy_render: Whether to cache static renders
            render_model: Optional model class for required context validation
        """
        self.name = template_name
        self._template = jinja_template
        self._lazy_render = lazy_render
        self._cached_render: str | None = None
        self._render_model = render_model

    def render(self, context_obj: Any | None = None, **kwargs: Any) -> str:
        """Render the prompt template with provided context.

        Args:
            context_obj: Object providing context attributes (required if render_model is set)
            **kwargs: Additional context variables

        Returns:
            Rendered prompt string

        Raises:
            TypeError: If required context object is missing or wrong type
        """
        render_context = kwargs.copy()

        if self._render_model:
            self._validate_and_add_context(context_obj, render_context)

        if self._should_use_cached_render(render_context):
            logger.debug("Using cached render for prompt '%s'", self.name)
            return self._cached_render

        final_prompt = self._template.render(**render_context)

        if self._lazy_render and not render_context:
            self._cached_render = final_prompt

        return final_prompt

    def _validate_and_add_context(
        self, context_obj: Any, render_context: dict[str, Any]
    ) -> None:
        """Validate context object and add its attributes to render context."""
        if context_obj is None:
            raise TypeError(
                f"Prompt '{self.name}' requires a context object of type "
                f"'{self._render_model.__name__}'"
            )

        if not isinstance(context_obj, self._render_model):
            raise TypeError(
                f"Expected context object of type '{self._render_model.__name__}', "
                f"got '{type(context_obj).__name__}'"
            )

        # Add public attributes from context object
        render_context.update(
            {
                key: value
                for key, value in vars(context_obj).items()
                if not key.startswith("_")
            }
        )

    def _should_use_cached_render(self, render_context: dict[str, Any]) -> bool:
        """Check if we should use cached render instead of re-rendering."""
        return (
            self._lazy_render and not render_context and self._cached_render is not None
        )


class PromptFile:
    """Descriptor that provides access to PromptTemplate instances.

    This descriptor loads and compiles prompt templates when accessed,
    providing a clean interface for template management.
    """

    def __init__(
        self,
        alias: str | None = None,
        lazy_render: bool = True,
        render_model: type | None = None,
    ) -> None:
        """Initialize a PromptFile descriptor.

        Args:
            alias: Optional filename (without extension) to use instead of attribute name
            lazy_render: Whether to cache static renders (disabled if render_model is set)
            render_model: Optional model class for required context validation
        """
        self.alias = alias
        self.render_model = render_model
        self.lazy_render = False if self.render_model else lazy_render
        self._filename: str = ""
        self._templates_loader: type | None = None
        self._jinja_env: Environment | None = None

    def __set_name__(self, owner: type, name: str) -> None:
        """Set the filename based on attribute name if alias not provided."""
        self._filename = self.alias or name

    def __get__(self, instance: Any, owner: type) -> PromptTemplate:
        """Load and return a PromptTemplate instance.

        Args:
            instance: The instance accessing the descriptor
            owner: The owner class

        Returns:
            Configured PromptTemplate instance

        Raises:
            TypeError: If the descriptor hasn't been properly configured
        """
        if self._templates_loader is None or self._jinja_env is None:
            raise TypeError(
                "PromptFile must be used within a class decorated with @prompt_loader"
            )

        template_content = getattr(self._templates_loader, self._filename)
        jinja_template = self._jinja_env.from_string(template_content)

        return PromptTemplate(
            template_name=self._filename,
            jinja_template=jinja_template,
            lazy_render=self.lazy_render,
            render_model=self.render_model,
        )


def prompt_loader(
    template_dir: str | Path,
    components: list[type],
    component_wrapper: WrapperStyle = WrapperStyle.NONE,
    prompt_helpers: dict[str, Callable[..., str]] | None = None,
    constants: object | None = None,
    lazy: bool = True,
) -> Callable[[type], type]:
    """Class decorator for hierarchical prompt template loading.

    This decorator configures a class to load and manage prompt templates
    with support for component inclusion, helper functions, and constants.

    Args:
        template_dir: Directory containing prompt template files
        components: List of component loader classes (decorated with @static_loader)
        component_wrapper: Style for wrapping included components
        prompt_helpers: Custom functions to make available in templates
        constants: Object whose public attributes become global template variables
        lazy: Whether to load templates lazily (always True for dynamic templates)

    Returns:
        Decorated class with configured PromptFile descriptors

    Raises:
        LoaderError: If configuration is invalid
    """

    def wrapper(cls: type) -> type:
        prompt_names = _collect_prompt_names(cls)
        _setup_prompt_descriptors(cls, prompt_names)

        jinja_env = _create_jinja_environment(
            components, component_wrapper, prompt_helpers, constants
        )

        templates_loader = _create_internal_templates_loader(template_dir, prompt_names)

        _configure_prompt_descriptors(cls, templates_loader, jinja_env, lazy)

        return cls

    return wrapper


def _collect_prompt_names(cls: type) -> list[str]:
    """Collect all prompt names from annotations and existing descriptors."""
    prompt_names = []

    # Add annotated attributes
    annotated_attrs = getattr(cls, "__annotations__", {})
    prompt_names.extend(annotated_attrs.keys())

    # Add existing PromptFile descriptors not in annotations
    for attr_name, attr_value in cls.__dict__.items():
        if isinstance(attr_value, PromptFile) and attr_name not in prompt_names:
            prompt_names.append(attr_name)

    return prompt_names


def _setup_prompt_descriptors(cls: type, prompt_names: list[str]) -> None:
    """Set up PromptFile descriptors for annotated attributes."""
    annotated_attrs = getattr(cls, "__annotations__", {})

    for attr_name in annotated_attrs:
        if attr_name not in cls.__dict__:
            setattr(cls, attr_name, PromptFile())


def _create_jinja_environment(
    components: list[type],
    component_wrapper: WrapperStyle,
    prompt_helpers: dict[str, Callable[..., str]] | None,
    constants: object | None,
) -> Environment:
    """Create and configure the Jinja2 environment."""
    jinja_env = Environment(
        loader=ComponentLoader(components, wrapper_style=component_wrapper),
        autoescape=False,
        undefined=StrictUndefined,
    )

    # Set up global functions and variables
    all_globals = {
        "few_shot": few_shot,
        "chain_of_thought": chain_of_thought,
        "react_step": react_step,
    }

    if prompt_helpers:
        all_globals.update(prompt_helpers)

    if constants:
        all_globals.update(
            {
                key: value
                for key, value in vars(constants).items()
                if not key.startswith("_")
            }
        )

    jinja_env.globals.update(all_globals)
    return jinja_env


def _create_internal_templates_loader(
    template_dir: str | Path, prompt_names: list[str]
) -> type:
    """Create the internal templates loader class."""

    @static_loader(root_dir=template_dir, file_type=FileType.PROMPT, lazy=True)
    class InternalTemplates:
        __annotations__ = {name: str for name in prompt_names}

    return InternalTemplates


def _configure_prompt_descriptors(
    cls: type, templates_loader: type, jinja_env: Environment, lazy: bool
) -> None:
    """Configure all PromptFile descriptors in the class."""
    for attr_name, attr_value in cls.__dict__.items():
        if isinstance(attr_value, PromptFile):
            if not lazy and attr_value.render_model:
                raise LoaderError(
                    f"Cannot eagerly load prompt '{attr_name}' because it "
                    "requires a dynamic render_model"
                )

            if not attr_value._filename:
                attr_value._filename = attr_value.alias or attr_name

            attr_value._templates_loader = templates_loader
            attr_value._jinja_env = jinja_env
