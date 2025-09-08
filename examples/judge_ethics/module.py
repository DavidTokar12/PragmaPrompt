from __future__ import annotations

from dataclasses import dataclass

from prompt_craft_kit import Component
from prompt_craft_kit import ComponentModule
from prompt_craft_kit import Prompt
from prompt_craft_kit import PromptModule


@dataclass
class Case:
    claim: str
    evidence: list[str]
    risk_notes: list[str]


@dataclass
class Verdict:
    decision: str
    reasoning: str
    risks: list[str]
    score: float


class EthicsComponents(ComponentModule[None]):
    fairness: Component
    bias_checks: Component
    privacy: Component
    safety: Component
    rubric: Component


class JudgeModule(PromptModule[None]):
    judge_utilitarian: Prompt[Case, Verdict]
    judge_deontological: Prompt[Case, Verdict]
