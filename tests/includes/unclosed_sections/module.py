from __future__ import annotations

from pragma_prompt import Prompt
from pragma_prompt import PromptModule


class UnclosedModule(PromptModule[None]):
    prompt_unclosed: Prompt[None, None]
