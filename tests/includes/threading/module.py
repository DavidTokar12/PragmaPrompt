from __future__ import annotations

from prompt_craft_kit import Prompt
from prompt_craft_kit import PromptModule


class ThreadingModule(PromptModule[None]):
    prompt_simple: Prompt[None, None]
