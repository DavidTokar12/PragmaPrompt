from __future__ import annotations

from enum import Enum


class PromptFileType(Enum):
    """Defines the supported prompt file types and their extensions."""

    SYSTEM = "system"
    USER = "user"
    COMPONENT = "component"
