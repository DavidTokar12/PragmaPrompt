from __future__ import annotations

from prompt_craft_kit import Component
from prompt_craft_kit import ComponentModule
from prompt_craft_kit import Prompt
from prompt_craft_kit import PromptModule


class ImportComponentModule(ComponentModule[None]):
    component_1: Component
    component_2: Component


class ImportPromptModule(PromptModule[None]):
    prompt_1: Prompt[None, None]
