from __future__ import annotations

import pragma_prompt as pp

from tests.includes.type_mismatch.module import TypedModule


ctx = TypedModule.mismatch_prompt.context
rm = TypedModule.mismatch_prompt.render_model

with pp.section("model"):
    f"{rm.name}"  # type: ignore[attr-defined]

with pp.section("context"):
    f"{ctx.project}"  # type: ignore[attr-defined]
