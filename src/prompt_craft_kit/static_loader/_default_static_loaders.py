# from __future__ import annotations

# import json

# from collections.abc import Callable
# from pathlib import Path
# from typing import Any

# from prompt_craft_kit.static_loader.static_file_type import StaticFileType


# def _default_json_parser(path: Path) -> Any:
#     """Default parser for JSON files that reads the file and decodes it."""
#     return json.loads(path.read_text("utf-8"))


# def _default_text_parser(path: Path) -> str:
#     """Default parser for plain text files."""
#     return path.read_text("utf-8")


# DEFAULT_PARSERS: dict[StaticFileType, Callable[[Path], Any]] = {
#     StaticFileType.JSON: _default_json_parser,
#     StaticFileType.MARKDOWN: _default_text_parser,
#     StaticFileType.TEXT: _default_text_parser,
# }
