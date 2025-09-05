from __future__ import annotations

import json

from collections.abc import Callable
from dataclasses import asdict
from dataclasses import is_dataclass
from pathlib import Path
from typing import Any

import dotenv
import openai
import pytest

from pydantic import BaseModel
from pydantic import Field

from tests.review import ResultItem
from tests.review import Review
from tests.review import ReviewModule
from tests.review import ReviewResult
from tests.review import ReviewUser


ARTIFACTS_DIRNAME = "artifacts"
RESULTS_FILENAME = "results.json"


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--llm-review",
        action="store_true",
        default=False,
        help="Enable LLM-based structured review for renderer tests.",
    )
    parser.addoption(
        "--llm-model",
        action="store",
        default="gpt-4o-2024-08-06",
        help="OpenAI model to use for LLM review (default: gpt-4o-2024-08-06).",
    )


@pytest.fixture(scope="session")
def artifacts_dir() -> Path:
    base = Path(__file__).parent / ARTIFACTS_DIRNAME
    base.mkdir(exist_ok=True)
    return base


@pytest.fixture(scope="session")
def results_path(artifacts_dir: Path) -> Path:
    return artifacts_dir / RESULTS_FILENAME


@pytest.fixture(scope="session", autouse=True)
def ensure_results_json(results_path: Path) -> None:
    if not results_path.exists():
        results_path.write_text("[]", encoding="utf-8")


def _json_serializer(obj: Any) -> Any:
    """
    Custom JSON serializer for objects json.dumps doesn't know how to handle.
    Used with the `default` parameter in json.dumps().
    """
    if isinstance(obj, BaseModel):
        return obj.model_dump()
    if is_dataclass(obj):
        return asdict(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


@pytest.fixture
def write_case_markdown(
    artifacts_dir: Path,
) -> Callable[[str, str, dict[str, Any], str, str, Review | None], str]:
    """
    Write a markdown file for a single test case. Returns the relative filename.
    """

    def _write_md(
        renderer: str,
        case: str,
        input_params: dict[str, Any],
        output: str,
        expectation: str,
        review: Review | None,
    ) -> str:
        fname = f"{renderer}__{case}.md".replace(" ", "_")
        fpath = artifacts_dir / fname

        review_block = (
            [
                "## LLM Review",
                f"**Result:** {review.result.value}",
                f"**Formatting rating:** {review.formatting_rating}",
                "",
                "### Reasoning",
                "```",
                review.reasoning or "(none)",
                "```",
            ]
            if review is not None
            else [
                "## LLM Review",
                "**Result:** none",
            ]
        )

        md = [
            f"# Renderer: {renderer}",
            f"**Case:** {case}",
            "",
            "## Input Params",
            "```json",
            json.dumps(
                input_params, ensure_ascii=False, indent=2, default=_json_serializer
            ),
            "```",
            "",
            "## Output",
            "```",
            output,
            "```",
            "",
            "## Expectation",
            expectation,
            "",
            *review_block,
            "",
        ]

        fpath.write_text("\n".join(md), encoding="utf-8")
        return fname

    return _write_md


@pytest.fixture
def append_results(results_path: Path) -> Callable[[str, Review | None], None]:
    """
    Append a summary record to results.json (list of objects).
    Stores {"file": <md filename>, "review": <Review | null>}
    """

    def _append(file: str, review: Review | None) -> None:
        raw = results_path.read_text(encoding="utf-8")
        data = json.loads(raw)
        if not isinstance(data, list):
            raise RuntimeError("results.json is unreadable or invalid (not a list)")

        item = ResultItem(file=file, review=review)
        data.append(asdict(item))
        results_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    return _append


@pytest.fixture
def llm_review(
    request: pytest.FixtureRequest,
) -> Callable[[str, str, dict[str, Any], str, str], Review | None]:
    """
    LLM review using OpenAI structured output.
    - Returns Review when --llm-review is enabled.
    - Returns None when --llm-review is not enabled.
    - Raises on any API/parse error when enabled (no silent failures).
    """
    enabled: bool = bool(request.config.getoption("--llm-review"))
    model: str = str(request.config.getoption("--llm-model"))

    class _ReviewModel(BaseModel):
        result: ReviewResult
        reasoning: str
        formatting_rating: int = Field(ge=1, le=10)

    def _review(
        renderer: str,
        case: str,
        input_params: dict[str, Any],
        output: str,
        expectation: str,
    ) -> Review | None:
        if not enabled:
            return None

        dotenv.load_dotenv()
        client = openai.OpenAI()

        render_model = ReviewUser(
            test_case=case,
            input_params=json.dumps(
                input_params, ensure_ascii=False, default=_json_serializer
            ),
            expectation=expectation,
            output=output,
        )

        with open("user.txt", "w") as f:
            f.write(ReviewModule.review_user.render(render_model=render_model))

        completion = client.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": ReviewModule.review_system.render()},
                {
                    "role": "user",
                    "content": ReviewModule.review_user.render(
                        render_model=render_model
                    ),
                },
            ],
            response_format=_ReviewModel,
            temperature=0,
        )

        parsed: _ReviewModel | None = completion.choices[0].message.parsed

        assert parsed is not None

        return Review(
            result=parsed.result,
            reasoning=parsed.reasoning,
            formatting_rating=parsed.formatting_rating,
        )

    return _review
