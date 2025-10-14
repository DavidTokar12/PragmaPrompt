from __future__ import annotations

from datetime import datetime
from pathlib import Path

from tests.includes.multi_renderer_prompt.module import MultiRendererPromptModule
from tests.includes.multi_renderer_prompt.module import PContext
from tests.includes.multi_renderer_prompt.module import PRenderModel


SAVE_RENDER_PLANS = True


def test_multi_renderer_prompt() -> None:
    context = PContext(user_id="test_user", items=["item1", "item2", "item3"])
    render_model = PRenderModel(template_name="test_template", timestamp=datetime.now())

    # Call render() which should generate and cache the plan
    output = MultiRendererPromptModule.multi_renderer_prompt.render(
        context=context, render_model=render_model
    )

    # Get the plan directly
    render_plan = MultiRendererPromptModule.multi_renderer_prompt.plan

    assert render_plan is not None

    # Check expected order of renderers
    assert [call.renderer for call in render_plan.calls] == [
        "block",
        "block",
        "section_start",
        "table",
        "section_end",
        "section_start",
        "code",
        "section_end",
        "section_start",
        "block",
        "block",
        "section_end",
    ]

    # Verify the output matches what we'd get from the plan
    assert output == render_plan.to_text()

    # If enabled, save the plan to file
    if SAVE_RENDER_PLANS:
        test_name = "multi_renderer_prompt"
        save_path = Path(__file__).parent / "test_artifacts" / f"{test_name}_plan.json"
        save_path.parent.mkdir(exist_ok=True)
        save_path.write_text(render_plan.model_dump_json(indent=2))
