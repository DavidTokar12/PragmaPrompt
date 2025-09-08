from __future__ import annotations

import prompt_craft_kit as pck

from tests.includes.type_mismatch.module import TypedModule


ctx = TypedModule.mismatch_prompt.context
rm = TypedModule.mismatch_prompt.render_model

with pck.section("model"):
    f"{rm.name}"  # type: ignore[attr-defined]

with pck.section("context"):
    f"{ctx.project}"  # type: ignore[attr-defined]
