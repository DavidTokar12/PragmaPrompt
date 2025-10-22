from __future__ import annotations

from dataclasses import dataclass

from pragma_prompt import Component
from pragma_prompt import ComponentModule
from pragma_prompt import Prompt
from pragma_prompt import PromptModule


@dataclass
class ExampleRenderModel:
    topic: str
    tone: str


class RenderModelComponents(ComponentModule[None]):
    uses_render_model: Component[ExampleRenderModel]


class RenderModelPrompts(PromptModule[None]):
    example: Prompt[None, ExampleRenderModel]
