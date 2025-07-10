"""PromptCraft Kit - A toolkit for hierarchical prompt management."""

from __future__ import annotations

from prompt_craft_kit.exceptions import ConfigurationError
from prompt_craft_kit.exceptions import LoaderError
from prompt_craft_kit.exceptions import ParsingError
from prompt_craft_kit.exceptions import TemplateError
from prompt_craft_kit.file_type import FileType
from prompt_craft_kit.prompt_helpers import chain_of_thought
from prompt_craft_kit.prompt_helpers import few_shot
from prompt_craft_kit.prompt_helpers import react_step
from prompt_craft_kit.prompt_loader import ComponentLoader
from prompt_craft_kit.prompt_loader import PromptFile
from prompt_craft_kit.prompt_loader import PromptTemplate
from prompt_craft_kit.prompt_loader import prompt_loader
from prompt_craft_kit.static_descriptor import StaticFile
from prompt_craft_kit.static_loader import static_loader
from prompt_craft_kit.wrapper_styles import WrapperStyle


__version__ = "0.1.0"

__all__ = [
    # Core loading functionality
    "static_loader",
    "prompt_loader",
    # Descriptors
    "StaticFile",
    "PromptFile",
    # Template classes
    "PromptTemplate",
    "ComponentLoader",
    # Enums
    "FileType",
    "WrapperStyle",
    # Helper functions
    "few_shot",
    "chain_of_thought",
    "react_step",
    # Exceptions
    "LoaderError",
    "ConfigurationError",
    "ParsingError",
    "TemplateError",
]
