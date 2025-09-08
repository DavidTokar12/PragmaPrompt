from __future__ import annotations

from prompt_craft_kit import Prompt
from prompt_craft_kit import PromptModule


class UnclosedModule(PromptModule[None]):
    prompt_unclosed: Prompt[None, None]
