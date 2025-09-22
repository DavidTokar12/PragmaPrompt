from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from pragma_prompt import Prompt
from pragma_prompt import PromptModule


class ReviewResult(str, Enum):
    PASS = "pass"
    ROOM_FOR_IMPROVEMENT = "room for improvement"
    FAIL = "fail"


@dataclass
class Review:
    result: ReviewResult
    reasoning: str
    formatting_rating: int


@dataclass
class ResultItem:
    file: str
    review: Review | None


@dataclass
class ReviewUser:
    test_case: str
    input_params: str
    expectation: str
    output: str


class ReviewModule(PromptModule[None]):
    module_dir = Path(__file__).parent

    review_system: Prompt[None, None] = Prompt(filename="review_system")
    review_user: Prompt[None, ReviewUser]
