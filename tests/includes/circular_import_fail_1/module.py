from __future__ import annotations

from pragma_prompt import Component
from pragma_prompt import ComponentModule


class CircularImportModule(ComponentModule[None]):
    component_1: Component[None]
    component_2: Component[None]
