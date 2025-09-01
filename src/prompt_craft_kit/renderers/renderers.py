from __future__ import annotations

from enum import Enum


class Renderers(str, Enum):
    BLOCK = "block"
    OUTPUT_FORMAT = "output_format"
    SHOT = "shot"
    SECTION_START = "section_start"
    SECTION_END = "section_end"
    WARNING = "warning"
    SEPARATOR = "separator"
    KV = "kv"
    CONSTRAINTS = "constraints"
    CODE = "code"
    TABLE = "table"
