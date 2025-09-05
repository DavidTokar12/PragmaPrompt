from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest

from pydantic import BaseModel
from pydantic import Field

from prompt_craft_kit import ToolStep
from prompt_craft_kit import shot
from prompt_craft_kit.runtime_context import session


class UserProfile(BaseModel):
    username: str
    expertise_level: str = Field(description="User's familiarity with the subject")


class SearchQuery(BaseModel):
    query: str
    domain: str = "finance"


class SearchResult(BaseModel):
    url: str
    title: str
    snippet: str


class FinalAnswer(BaseModel):
    summary: str
    key_takeaways: list[str]
    confidence_score: float


CASES = [
    # Case 1: Minimal shot with only required arguments
    (
        {
            "user": "What is the capital of Switzerland?",
            "output": "Bern",
        },
        "This is a minimal prompt shot with only a user message and a string output. Review the basic formatting for simplicity and clarity.",
        "minimal_shot",
    ),
    # Case 2: Shot with added Context and structured Input
    (
        {
            "user": "What's the outlook for this company?",
            "context": UserProfile(username="investor_bob", expertise_level="beginner"),
            "input": {"company_ticker": "TCORP", "timeframe": "6 months"},
            "output": "The outlook is positive, but volatile.",
        },
        "This shot includes a structured context and input. Review how these blocks are formatted and separated from the main user prompt and output.",
        "shot_with_context_and_input",
    ),
    # Case 3: Shot demonstrating a Chain of Thought process
    (
        {
            "user": "Write a short poem about the moon.",
            "thought": "The user wants a poem. I will think about themes like light, night, and loneliness. I will structure it in three short stanzas.",
            "output": "Silver orb in velvet night,\nA silent watchman, pure and bright,\nGuiding sailors with its light.",
        },
        "This shot includes a 'Thought' block. Review its placement and formatting to ensure it clearly represents a step before the final output.",
        "shot_with_thought",
    ),
    # Case 4: Shot with a single, simple tool call
    (
        {
            "user": "Search for today's top finance news.",
            "tools": [
                ToolStep(
                    name="web_search",
                    rationale="The user is asking for current news, so I need to use the web search tool.",
                    input=SearchQuery(query="top finance news today"),
                    output=[
                        SearchResult(
                            url="news.com/1",
                            title="Market Hits New High",
                            snippet="...",
                        )
                    ],
                )
            ],
            "output": {
                "summary": "The market reached a new high today, driven by tech stocks."
            },
        },
        "This shot demonstrates a single tool call. Review the 'Tool call chain' formatting, especially indentation and the clarity of the rationale, input, and output.",
        "shot_with_single_tool",
    ),
    # Case 5: The "Kitchen Sink" - a complex, multi-step tool chain
    (
        {
            "title": "Example: Research and Summarize Financial Report",
            "context": UserProfile(username="analyst_jane", expertise_level="expert"),
            "user": "Please find the latest quarterly earnings report for 'TechCorp' and provide a summary with key takeaways.",
            "tools": [
                ToolStep(
                    name="web_search",
                    rationale="I need to find the official press release.",
                    input=SearchQuery(
                        query="TechCorp latest quarterly earnings report"
                    ),
                    output=[
                        SearchResult(
                            url="investors.techcorp.com/q3-2025-earnings",
                            title="TechCorp Reports Q3 2025",
                            snippet="...",
                        )
                    ],
                    thought="The first result is the official source. I will use this.",
                ),
                ToolStep(
                    name="summarize_document",
                    rationale="Now I will summarize the document to extract key points.",
                    input={"url": "investors.techcorp.com/q3-2025-earnings"},
                    output={
                        "summary": "Strong earnings driven by cloud division.",
                        "takeaways": ["Revenue hit $50B."],
                    },
                ),
            ],
            "thought": "The tool chain was successful. I will format the final answer.",
            "output": FinalAnswer(
                summary="TechCorp reported record revenue of $50 billion in Q3 2025, fueled by its cloud services division.",
                key_takeaways=[
                    "Record Q3 revenue of $50 billion.",
                    "Cloud division growth of 25% YoY.",
                ],
                confidence_score=0.95,
            ),
        },
        "This is a complex shot with all possible components. Review the overall structure, formatting, and readability. Pay close attention to how all the different blocks (context, tools, thought, output) work together.",
        "complex_tool_chain_shot",
    ),
]


@pytest.mark.llm
@pytest.mark.parametrize("kwargs, description, case", CASES, ids=[c[-1] for c in CASES])
def test_shot_cases(
    kwargs: dict[str, Any],
    description: str,
    case: str,
    llm_review: Callable,
    write_case_markdown: Callable,
    append_results: Callable,
) -> None:
    """
    Tests the shot renderer with progressively complex scenarios,
    relying on an LLM to evaluate the quality of the output formatting.
    """
    with session():
        out = shot(**kwargs)

    review = llm_review(
        renderer="shot",
        case=case,
        input_params=kwargs,
        output=out,
        expectation=description,
    )

    md_file = write_case_markdown(
        renderer="shot",
        case=case,
        input_params=kwargs,
        output=out,
        expectation=description,
        review=review,
    )

    append_results(file=md_file, review=review)
