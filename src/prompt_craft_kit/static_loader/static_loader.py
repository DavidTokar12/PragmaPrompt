# from __future__ import annotations

# import logging

# from collections.abc import Callable
# from pathlib import Path
# from typing import Any
# from typing import TypeVar

# from prompt_craft_kit.exceptions import LoaderError
# from prompt_craft_kit.static_loader._default_static_loaders import DEFAULT_PARSERS
# from prompt_craft_kit.static_loader.static_descriptor import StaticFile
# from prompt_craft_kit.static_loader.static_file_type import StaticFileType
# from prompt_craft_kit.utils import validate_path


# T = TypeVar("T")

# logger = logging.getLogger(__name__)


# def setup_class_descriptors(
#     cls: type,
#     descriptor_class: type,
#     annotated_attrs: dict[str, Any],
# ) -> list[str]:
#     """Set up descriptors for annotated attributes that don't have values.

#     Args:
#         cls: The class to modify
#         descriptor_class: The descriptor class to instantiate
#         annotated_attrs: Dictionary of annotated attributes

#     Returns:
#         List of descriptor names that were set up
#     """
#     descriptor_names = []

#     for attr_name in annotated_attrs:
#         if attr_name not in cls.__dict__:
#             setattr(cls, attr_name, descriptor_class())
#             descriptor_names.append(attr_name)

#     return descriptor_names


# def configure_descriptor(
#     descriptor: Any,
#     attr_name: str,
#     root_dir: Path,
#     parser: Callable[[Path], Any],
#     file_suffix: str,
#     cache: dict[str, Any],
# ) -> None:
#     """Configure a descriptor with the necessary settings.

#     Args:
#         descriptor: The descriptor instance to configure
#         attr_name: The attribute name
#         root_dir: The root directory for files
#         parser: The parser function
#         file_suffix: The file extension
#         cache: The shared cache dictionary
#     """
#     if not descriptor._filename:
#         descriptor._filename = descriptor.alias or attr_name

#     descriptor._root_dir = root_dir
#     descriptor._parser = parser
#     descriptor._file_suffix = file_suffix
#     descriptor._cache = cache


# def eager_load_descriptors(cls: type, descriptor_names: list[str]) -> None:
#     """Eagerly load all descriptors for a class.

#     Args:
#         cls: The class containing the descriptors
#         descriptor_names: List of descriptor attribute names

#     Raises:
#         LoaderError: If eager loading fails
#     """
#     logger.debug("Eagerly loading assets for class '%s'", cls.__name__)

#     for attr_name in descriptor_names:
#         try:
#             getattr(cls, attr_name)
#         except Exception as e:
#             raise LoaderError(
#                 f"Eager loading failed for '{attr_name}' in class '{cls.__name__}'"
#             ) from e


# def static_loader(
#     root_dir: str | Path,
#     file_type: StaticFileType,
#     parser: Callable[[Path], T] | None = None,
#     lazy: bool = True,
# ) -> Callable[[type], type]:
#     """
#     Class decorator that configures Static descriptors for lazy file loading.

#     This decorator sets up a class to automatically load static files when
#     their corresponding attributes are accessed. It supports various file types
#     and can use custom parsers.

#     Args:
#         root_dir: Directory containing the static files
#         file_type: Type of files to load (determines default parser and extension)
#         parser: Optional custom parser function. If not provided, uses default
#                 parser for the file type
#         lazy: If False, all files are loaded immediately during decoration.
#               If True, files are loaded on first access

#     Returns:
#         Decorated class with configured Static descriptors

#     Raises:
#         LoaderError: If eager loading fails or configuration is invalid
#     """

#     def wrapper(cls: type) -> type:
#         resolved_root = validate_path(root_dir)
#         shared_cache: dict[str, Any] = {}
#         cls._static_file_cache = shared_cache

#         final_parser = parser or DEFAULT_PARSERS[file_type]

#         annotated_attrs = getattr(cls, "__annotations__", {})
#         descriptor_names = setup_class_descriptors(cls, StaticFile, annotated_attrs)

#         for attr_name, attr_value in cls.__dict__.items():
#             if isinstance(attr_value, StaticFile):
#                 configure_descriptor(
#                     attr_value,
#                     attr_name,
#                     resolved_root,
#                     final_parser,
#                     file_type.value,
#                     shared_cache,
#                 )
#                 if attr_name not in descriptor_names:
#                     descriptor_names.append(attr_name)

#         if not lazy:
#             eager_load_descriptors(cls, descriptor_names)

#         return cls

#     return wrapper
