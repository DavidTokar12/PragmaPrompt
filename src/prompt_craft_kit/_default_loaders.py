from __future__ import annotations

import json

from typing import TYPE_CHECKING
from typing import Any

from prompt_craft_kit.file_type import FileType


if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path


def _default_json_parser(path: Path) -> Any:
    """Default parser for JSON files that reads the file and decodes it."""
    return json.loads(path.read_text("utf-8"))


def _default_text_parser(path: Path) -> str:
    """Default parser for plain text files."""
    return path.read_text("utf-8")


DEFAULT_PARSERS: dict[FileType, Callable[[Path], Any]] = {
    FileType.JSON: _default_json_parser,
    FileType.MARKDOWN: _default_text_parser,
    FileType.PROMPT: _default_text_parser,
}
