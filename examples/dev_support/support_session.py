from __future__ import annotations

import prompt_craft_kit as pck

from examples.dev_support.module import SupportModule, SupportComponents


ctx = SupportModule.support_session.context
rm = SupportModule.support_session.render_model

"""
Ultra-compact, dynamic support session for programmers.
- Demonstrates: dynamic sections, separator, table(csv), output_format, components.
"""

# Bring in components (render into current session)
SupportComponents.ethics.render()
SupportComponents.healthy_defaults.render()
SupportComponents.gratitude_nudge.render()
SupportComponents.breathing_exercise.render()


# Mood logic based on KPIs (tiny and readable). Real-world prompts can be dynamic.
mood = "celebratory"
if ctx.test_coverage < 55 or ctx.deploys_failed > 0:
    mood = "gentle"
elif ctx.prs_open > 7:
    mood = "focused"
elif ctx.caffeine_level > 5:
    mood = "hydration_reminder"


with pck.section("summary"):
    f"bugs_last_week: {ctx.bugs_last_week}"
    f"prs_open: {ctx.prs_open}"
    f"test_coverage: {ctx.test_coverage}%"
    f"deploys_failed: {ctx.deploys_failed}"
    f"caffeine_level: {ctx.caffeine_level} cups"

pck.separator(f"MOOD: {mood.upper()}")

with pck.section("advice"):
    if mood == "gentle":
        """Start small. One passing test. One flaky test quarantined. One bug closed."""
    elif mood == "focused":
        """Merge PRs in batches of 2. Add labels. Ask for 1 reviewer per PR."""
    elif mood == "hydration_reminder":
        """Push code, then push water. Swap 1 coffee for water this hour."""
    else:
        """High-five. Ship something delightful. Keep the scope tiny and reversible."""


# Minimal plan as CSV table (CSV avoids optional 'prettytable' dependency)
pck.table(
    rows=[
        ("5 min", "breathing_exercise"),
        ("25 min", "focus: highest-impact bug"),
        ("5 min", "gratitude_nudge"),
    ],
    headers=["slot", "action"],
    fmt="csv",
)


pck.separator("OUTPUT FORMAT")

pck.output_format(
    {
        "mood": "",
        "advice": ["..."],
        "one_day_plan": ["..."],
        "five_min_exercise": "...",
    }
)

with pck.section("result"):
    f"<mood>{mood}</mood>"
    """
    <advice>
      <item>...</item>
      <item>...</item>
    </advice>
    <one_day_plan>
      <item>...</item>
    </one_day_plan>
    <five_min_exercise>breathing_exercise</five_min_exercise>
    """
