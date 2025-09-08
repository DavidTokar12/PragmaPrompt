from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass
class PromptSection:
    body: str
    renderer: str
    input_params: dict[str, Any] = field(default_factory=dict)
