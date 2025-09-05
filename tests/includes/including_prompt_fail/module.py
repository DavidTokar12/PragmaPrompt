from __future__ import annotations

from prompt_craft_kit import Prompt
from prompt_craft_kit import PromptModule


class ImportPromptModule(PromptModule[None]):
    prompt_1: Prompt
    prompt_2: Prompt
