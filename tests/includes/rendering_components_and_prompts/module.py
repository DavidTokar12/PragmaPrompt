from __future__ import annotations

from pragma_prompt import Component
from pragma_prompt import ComponentModule
from pragma_prompt import Prompt
from pragma_prompt import PromptModule


class ImportComponentModule(ComponentModule[None]):
    component_1: Component[None]
    component_2: Component[None]


class ImportPromptModule(PromptModule[None]):
    prompt_1: Prompt[None, None]
