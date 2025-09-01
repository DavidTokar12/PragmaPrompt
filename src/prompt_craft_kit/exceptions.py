from __future__ import annotations


class LoaderError(Exception):
    """Base exception for errors related to file and prompt loading operations."""


class FileNotFoundError(LoaderError):
    """Raised when a required file cannot be found."""


class ParsingError(LoaderError):
    """Raised when a file cannot be parsed correctly."""


class ConfigurationError(LoaderError):
    """Raised when loader configuration is invalid."""
