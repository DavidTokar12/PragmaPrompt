from __future__ import annotations

import prompt_craft_kit as pck

from examples.judge_ethics.module import JudgeModule, EthicsComponents


ctx = JudgeModule.judge_utilitarian.context
rm = JudgeModule.judge_utilitarian.render_model

"""
Judge A (Utilitarian): maximize net benefit; tolerate minor downsides if total harm decreases.
Demonstrates: section(), separator(), shot(), output_format(), section_start/end.
"""

EthicsComponents.fairness.render()
EthicsComponents.bias_checks.render()
EthicsComponents.privacy.render()
EthicsComponents.safety.render()
EthicsComponents.rubric.render()


with pck.section("case"):
    f"claim: {ctx.claim}"
    pck.table(
        rows=[(i + 1, ev) for i, ev in enumerate(ctx.evidence)],
        headers=["#", "evidence"],
        fmt="csv",
    )

pck.separator("EXAMPLE")

pck.shot(
    user="Approve a harmless feature that reduces two support escalations/week?",
    output="approve (small benefit, negligible risk)",
)

pck.separator("OUTPUT FORMAT")

pck.output_format(
    {
        "decision": "approve|reject|revise",
        "reasoning": "",
        "risks": ["..."],
        "score": 0.0,
    }
)

# Show explicit section_start/end (works like with section(), but manual)
pck.section_start("verdict")
"""
<decision>...</decision>
<reasoning>...</reasoning>
<risks>
  <item>...</item>
</risks>
<score>0.0..1.0</score>
"""
pck.section_end("verdict")
