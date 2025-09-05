from __future__ import annotations

from prompt_craft_kit import Component
from prompt_craft_kit import ComponentModule


class CircularImportModule(ComponentModule[None]):
    component_1: Component
    component_2: Component
