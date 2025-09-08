from __future__ import annotations

import prompt_craft_kit as pck

from examples.judge_ethics.module import JudgeModule, EthicsComponents


ctx = JudgeModule.judge_deontological.context
rm = JudgeModule.judge_deontological.render_model

"""
Judge B (Deontological): duty and rules first; consequences matter less than principles.
Demonstrates: warnings, kv-based rule summary, shot for borderline case.
"""

EthicsComponents.fairness.render()
EthicsComponents.privacy.render()
EthicsComponents.safety.render()


pck.warning(
    title="Primary duty",
    level=2,
    body="If a rule forbids it, reject—even if net benefit is high.",
)

pck.kv(
    {
        "rule_hierarchy": "safety > privacy > fairness > utility",
        "tie_breaker": "default to reject if duties conflict",
    }
)

with pck.section("case"):
    f"claim: {ctx.claim}"
    pck.table(
        rows=[(i + 1, ev) for i, ev in enumerate(ctx.evidence)],
        headers=["#", "evidence"],
        fmt="csv",
    )

pck.shot(
    user="Feature helps most users but violates a privacy rule.",
    output="reject (rule violation outweighs aggregate benefit)",
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

with pck.section("verdict"):
    """
    <decision>...</decision>
    <reasoning>...</reasoning>
    <risks>
      <item>...</item>
      <item>...</item>
    </risks>
    <score>0.0..1.0</score>
    """
