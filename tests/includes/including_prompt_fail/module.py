from __future__ import annotations

from pragma_prompt import Prompt
from pragma_prompt import PromptModule


class ImportPromptModule(PromptModule[None]):
    prompt_1: Prompt[None, None]
    prompt_2: Prompt[None, None]
