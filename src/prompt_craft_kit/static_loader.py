"""Static file loader decorator for lazy loading of static assets."""

from __future__ import annotations

import logging

from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any
from typing import TypeVar

from prompt_craft_kit._default_loaders import DEFAULT_PARSERS
from prompt_craft_kit.file_type import FileType
from prompt_craft_kit.static_descriptor import StaticFile
from prompt_craft_kit.utils import configure_descriptor
from prompt_craft_kit.utils import eager_load_descriptors
from prompt_craft_kit.utils import setup_class_descriptors
from prompt_craft_kit.utils import validate_path


if TYPE_CHECKING:
    from collections.abc import Callable

T = TypeVar("T")

logger = logging.getLogger(__name__)


def static_loader(
    root_dir: str | Path,
    file_type: FileType,
    parser: Callable[[Path], T] | None = None,
    lazy: bool = True,
) -> Callable[[type], type]:
    """Class decorator that configures Static descriptors for lazy file loading.

    This decorator sets up a class to automatically load static files when
    their corresponding attributes are accessed. It supports various file types
    and can use custom parsers.

    Args:
        root_dir: Directory containing the static files
        file_type: Type of files to load (determines default parser and extension)
        parser: Optional custom parser function. If not provided, uses default
                parser for the file type
        lazy: If False, all files are loaded immediately during decoration.
              If True, files are loaded on first access

    Returns:
        Decorated class with configured Static descriptors

    Raises:
        LoaderError: If eager loading fails or configuration is invalid
    """

    def wrapper(cls: type) -> type:
        resolved_root = validate_path(root_dir)
        shared_cache: dict[str, Any] = {}
        cls._static_file_cache = shared_cache

        final_parser = parser or DEFAULT_PARSERS[file_type]

        # Set up descriptors for annotated attributes
        annotated_attrs = getattr(cls, "__annotations__", {})
        descriptor_names = setup_class_descriptors(cls, StaticFile, annotated_attrs)

        # Configure existing descriptors
        for attr_name, attr_value in cls.__dict__.items():
            if isinstance(attr_value, StaticFile):
                configure_descriptor(
                    attr_value,
                    attr_name,
                    resolved_root,
                    final_parser,
                    file_type.value,
                    shared_cache,
                )
                if attr_name not in descriptor_names:
                    descriptor_names.append(attr_name)

        # Eager load if requested
        if not lazy:
            eager_load_descriptors(cls, descriptor_names)

        return cls

    return wrapper
