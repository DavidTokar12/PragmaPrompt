from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from prompt_craft_kit.renderers.renderers import Renderers


@dataclass
class PromptSection:
    body: str
    renderer: Renderers
    input_params: dict[str, Any] = field(default_factory=dict)
