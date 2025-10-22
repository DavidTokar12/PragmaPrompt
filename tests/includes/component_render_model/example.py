from __future__ import annotations

from tests.includes.component_render_model.module import RenderModelComponents
from tests.includes.component_render_model.module import RenderModelPrompts


rm = RenderModelPrompts.example.render_model

RenderModelComponents.uses_render_model.render()

f"[prompt] topic={getattr(rm, 'topic', 'unknown')}; tone={getattr(rm, 'tone', 'unknown')}"
