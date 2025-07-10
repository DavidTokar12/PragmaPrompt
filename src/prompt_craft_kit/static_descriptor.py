"""Static file descriptor for lazy loading of static assets."""

from __future__ import annotations

import logging

from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any
from typing import Generic
from typing import TypeVar

from prompt_craft_kit.exceptions import ConfigurationError
from prompt_craft_kit.exceptions import LoaderError


if TYPE_CHECKING:
    from collections.abc import Callable

T = TypeVar("T")

logger = logging.getLogger(__name__)


class StaticFile(Generic[T]):
    """A descriptor for lazy-loading and caching static file content.

    This descriptor is designed to be used as a class attribute within classes
    decorated with `@static_loader`. It handles lazy loading of files and caches
    the parsed content for subsequent accesses.
    """

    def __init__(self, alias: str | None = None) -> None:
        """Initialize the Static descriptor.

        Args:
            alias: Optional filename (without extension) to use instead of the
                   attribute name. If not provided, the attribute name will be
                   used as the filename.
        """
        self.alias = alias
        self._filename: str = ""
        self._cache: dict[str, T] | None = None
        self._root_dir: Path | None = None
        self._parser: Callable[[Path], T] | None = None
        self._file_suffix: str | None = None

    def __set_name__(self, owner: type, name: str) -> None:
        """Called when the descriptor is assigned to a class attribute.

        This captures the attribute name to use as the default filename.
        """
        self._filename = self.alias or name

    def __get__(self, instance: Any, owner: type) -> T:
        """Load and return the file content when the attribute is accessed.

        Args:
            instance: The instance accessing the attribute (can be None for class access)
            owner: The class that owns this descriptor

        Returns:
            The parsed content of the file

        Raises:
            ConfigurationError: If the class hasn't been properly decorated
            FileNotFoundError: If the file doesn't exist
            LoaderError: If file loading or parsing fails
        """
        self._validate_configuration(owner)

        if self._filename in self._cache:
            return self._cache[self._filename]

        return self._load_and_cache_file()

    def _validate_configuration(self, owner: type) -> None:
        """Validate that the descriptor has been properly configured."""
        if (
            self._cache is None
            or self._root_dir is None
            or self._parser is None
            or self._file_suffix is None
        ):
            raise ConfigurationError(
                f"Class '{owner.__name__}' containing attribute '{self._filename}' "
                "must be decorated with @static_loader"
            )

    def _load_and_cache_file(self) -> T:
        """Load the file content and cache it for future access."""
        full_path = self._root_dir / f"{self._filename}{self._file_suffix}"
        logger.debug("Loading static file: %s", full_path)

        if not full_path.is_file():
            raise FileNotFoundError(f"Static file not found: {full_path}")

        try:
            parsed_data = self._parser(full_path)
            self._cache[self._filename] = parsed_data
            return parsed_data
        except Exception as e:
            raise LoaderError(f"Failed to load or parse file {full_path}") from e
