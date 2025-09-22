from __future__ import annotations

from pragma_prompt import Prompt
from pragma_prompt import PromptModule


class ThreadingModule(PromptModule[None]):
    prompt_simple: Prompt[None, None]
