from __future__ import annotations

from prompt_craft_kit import Prompt
from prompt_craft_kit import PromptModule


class TypedModule(PromptModule[None]):
    mismatch_prompt: Prompt[object, object]
