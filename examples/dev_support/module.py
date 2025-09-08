from __future__ import annotations

from dataclasses import dataclass

from prompt_craft_kit import Component
from prompt_craft_kit import ComponentModule
from prompt_craft_kit import Prompt
from prompt_craft_kit import PromptModule


@dataclass
class DevKPIs:
    bugs_last_week: int
    prs_open: int
    test_coverage: float  # 0..100
    deploys_failed: int
    caffeine_level: int  # cups today


@dataclass
class SupportOutput:
    mood: str
    advice: list[str]
    one_day_plan: list[str]
    five_min_exercise: str


class SupportComponents(ComponentModule[None]):
    ethics: Component
    healthy_defaults: Component
    gratitude_nudge: Component
    breathing_exercise: Component


class SupportModule(PromptModule[None]):
    support_session: Prompt[DevKPIs, SupportOutput]
