from __future__ import annotations

from tests.includes.component_render_model.module import ExampleRenderModel
from tests.includes.component_render_model.module import RenderModelComponents
from tests.includes.component_render_model.module import RenderModelPrompts


def test_component_render_accepts_render_model() -> None:
    rm = ExampleRenderModel(topic="growth hacking", tone="irreverent")

    output = RenderModelComponents.uses_render_model.render(render_model=rm)

    assert output.strip() == "[component] topic=growth hacking; tone=irreverent"


def test_component_render_in_prompt_shares_render_model() -> None:
    rm = ExampleRenderModel(topic="growth hacking", tone="irreverent")

    rendered = RenderModelPrompts.example.render(render_model=rm)

    assert "[component] topic=growth hacking; tone=irreverent" in rendered
    assert "[prompt] topic=growth hacking; tone=irreverent" in rendered
