from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import overload

from prompt_craft_kit.renderers.render_function import render_function
from prompt_craft_kit.renderers.renderers import Renderers
from prompt_craft_kit.renderers.utils import LlmResponseLike
from prompt_craft_kit.renderers.utils import to_display_block


@dataclass(frozen=True)
class ToolStep:
    name: str
    rationale: str | None = None
    input: LlmResponseLike | None = None
    output: LlmResponseLike | None = None
    thought: str | None = None


def tool_step(
    name: str,
    *,
    rationale: str | None = None,
    input: LlmResponseLike | None = None,
    output: LlmResponseLike | None = None,
    thought: str | None = None,
) -> ToolStep:
    return ToolStep(
        name=name,
        rationale=rationale,
        input=input,
        output=output,
        thought=thought,
    )


# --- Helper functions for programmatic rendering ---


def _render_tagged_block(tag: str, content: LlmResponseLike) -> str:
    """Renders content inside XML-style tags."""
    formatted_content = to_display_block(content)
    if "\n" in formatted_content:
        return f"<{tag}>\n{formatted_content}\n</{tag}>"
    return f"<{tag}>{formatted_content}</{tag}>"


def _render_tool_step(step: ToolStep) -> str:
    """Renders a single tool step with all its components."""
    parts = ["<tool_step>"]
    parts.append(f"<name>{step.name}</name>")
    if step.rationale:
        parts.append(f"<rationale>{step.rationale}</rationale>")
    if step.input is not None:
        parts.append(_render_tagged_block("input", step.input))
    if step.output is not None:
        parts.append(_render_tagged_block("output", step.output))
    if step.thought:
        parts.append(f"<thought>{step.thought}</thought>")
    parts.append("</tool_step>")
    return "\n".join(parts)


# --- Main renderer function (No Jinja2) ---


@overload
def shot(*, user: str, output: LlmResponseLike) -> str: ...


@overload
def shot(
    *, user: str, output: LlmResponseLike, input: LlmResponseLike | None = ...
) -> str: ...


@overload
def shot(
    *,
    title: str | None = ...,
    context: LlmResponseLike | None = ...,
    user: str,
    input: LlmResponseLike | None = ...,
    tools: Sequence[ToolStep] = ...,
    thought: str | None = ...,
    output: LlmResponseLike,
) -> str: ...


@render_function(Renderers.SHOT)
def shot(
    *,
    title: str | None = None,
    context: LlmResponseLike | None = None,
    user: str,
    input: LlmResponseLike | None = None,
    tools: Sequence[ToolStep] = (),
    thought: str | None = None,
    output: LlmResponseLike,
) -> str:
    """
    Renders a single shot (example) by programmatically building the string.
    """
    main_parts = []

    if title:
        main_parts.append(f"### {title}")

    main_parts.append(f"User: {user}")

    if context is not None:
        main_parts.append(_render_tagged_block("context", context))

    if input is not None:
        main_parts.append(_render_tagged_block("input", input))

    if tools:
        tool_steps_str = "\n".join(_render_tool_step(step) for step in tools)
        main_parts.append(f"<tool_chain>\n{tool_steps_str}\n</tool_chain>")

    if thought:
        main_parts.append(_render_tagged_block("thought", thought))

    main_parts.append(_render_tagged_block("output", output))

    return "\n\n".join(main_parts)
