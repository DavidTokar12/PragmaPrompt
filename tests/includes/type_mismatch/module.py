from __future__ import annotations

from pragma_prompt import Prompt
from pragma_prompt import PromptModule


class TypedModule(PromptModule[None]):
    mismatch_prompt: Prompt[object, object]
