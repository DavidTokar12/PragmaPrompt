from __future__ import annotations

import prompt_craft_kit as pck


"""
Evaluation rubric used by both judges. JSON schema is shown for clarity.
"""

pck.code_block(
    '{\n  "decision": "approve|reject|revise",\n  "reasoning": "string",\n  "risks": ["string"],\n  "score": 0.0\n}',
    lang="json",
)

pck.table(
    rows=[
        ("evidence_quality", 0.4),
        ("risk_severity", 0.3),
        ("fairness_alignment", 0.2),
        ("privacy_compliance", 0.1),
    ],
    headers=["criterion", "weight"],
    fmt="csv",
)
