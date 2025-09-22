from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from pragma_prompt import Prompt
from pragma_prompt import PromptModule


@dataclass
class PContext:
    """Context for the multi-renderer prompt."""

    user_id: str
    items: list[Any]


class PRenderModel(BaseModel):
    """Render model for the multi-renderer prompt."""

    template_name: str
    timestamp: datetime


class MultiRendererPromptModule(PromptModule[None]):
    """Module containing prompts that demonstrate using different renderers."""

    module_dir = Path(__file__).parent
    multi_renderer_prompt: Prompt[PContext, PRenderModel]
