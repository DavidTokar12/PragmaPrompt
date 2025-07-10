from __future__ import annotations

from enum import Enum


class FileType(Enum):
    """Defines the supported static file types and their extensions."""

    JSON = ".json"
    MARKDOWN = ".md"
    PROMPT = ".prompt"
