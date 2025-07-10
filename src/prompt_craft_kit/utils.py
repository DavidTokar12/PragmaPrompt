"""Utility functions for the prompt-craft-kit package."""

from __future__ import annotations

import logging

from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any

from prompt_craft_kit.exceptions import ConfigurationError
from prompt_craft_kit.exceptions import LoaderError


if TYPE_CHECKING:
    from collections.abc import Callable

logger = logging.getLogger(__name__)


def validate_path(path: str | Path) -> Path:
    """Validate and resolve a path argument.

    Args:
        path: The path to validate

    Returns:
        The resolved Path object

    Raises:
        ConfigurationError: If the path is invalid
    """
    try:
        return Path(path).resolve()
    except Exception as e:
        raise ConfigurationError(f"Invalid path: {path}") from e


def setup_class_descriptors(
    cls: type,
    descriptor_class: type,
    annotated_attrs: dict[str, Any],
) -> list[str]:
    """Set up descriptors for annotated attributes that don't have values.

    Args:
        cls: The class to modify
        descriptor_class: The descriptor class to instantiate
        annotated_attrs: Dictionary of annotated attributes

    Returns:
        List of descriptor names that were set up
    """
    descriptor_names = []

    for attr_name in annotated_attrs:
        if attr_name not in cls.__dict__:
            setattr(cls, attr_name, descriptor_class())
            descriptor_names.append(attr_name)

    return descriptor_names


def configure_descriptor(
    descriptor: Any,
    attr_name: str,
    root_dir: Path,
    parser: Callable[[Path], Any],
    file_suffix: str,
    cache: dict[str, Any],
) -> None:
    """Configure a descriptor with the necessary settings.

    Args:
        descriptor: The descriptor instance to configure
        attr_name: The attribute name
        root_dir: The root directory for files
        parser: The parser function
        file_suffix: The file extension
        cache: The shared cache dictionary
    """
    if not descriptor._filename:
        descriptor._filename = descriptor.alias or attr_name

    descriptor._root_dir = root_dir
    descriptor._parser = parser
    descriptor._file_suffix = file_suffix
    descriptor._cache = cache


def eager_load_descriptors(cls: type, descriptor_names: list[str]) -> None:
    """Eagerly load all descriptors for a class.

    Args:
        cls: The class containing the descriptors
        descriptor_names: List of descriptor attribute names

    Raises:
        LoaderError: If eager loading fails
    """
    logger.debug("Eagerly loading assets for class '%s'", cls.__name__)

    for attr_name in descriptor_names:
        try:
            getattr(cls, attr_name)
        except Exception as e:
            raise LoaderError(
                f"Eager loading failed for '{attr_name}' in class '{cls.__name__}'"
            ) from e
