from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from pragma_prompt.renderers.render_function import render_function
from pragma_prompt.renderers.types import LlmResponseLike
from pragma_prompt.renderers.utils import to_display_block


@dataclass(frozen=True)
class ToolStep:
    """A single tool call step, for inclusion in a tool chain."""

    name: str
    rationale: str | None = None
    input: LlmResponseLike | None = None
    output: LlmResponseLike | None = None
    thought: str | None = None


def tool_step(
    name: str,
    *,
    rationale: str | None = None,
    input: LlmResponseLike | None = None,  # Back-compat alias (deprecated)
    tool_input: LlmResponseLike | None = None,
    output: LlmResponseLike | None = None,
    thought: str | None = None,
) -> ToolStep:
    """Helper to construct a :class:`ToolStep`.

    Args:
        name: Tool name.
        rationale: Optional rationale for invoking the tool.
        input: Deprecated alias of ``tool_input`` (kept for backward compatibility).
        tool_input: Input provided to the tool (preferred name).
        output: Tool output.
        thought: Optional thought/comment associated with this step.
    """
    if tool_input is None:
        tool_input = input
    return ToolStep(
        name=name,
        rationale=rationale,
        input=tool_input,
        output=output,
        thought=thought,
    )


def _render_tagged_block(tag: str, content: LlmResponseLike) -> str:
    """Renders content inside XML-style tags with unified formatting."""
    t = tag.upper()
    formatted = to_display_block(content)
    return f"<{t}>\n{formatted}\n</{t}>"


def _render_tool_step(step: ToolStep) -> str:
    """Renders a single tool step with all its components."""
    parts = ["<TOOL_STEP>"]
    parts.append(_render_tagged_block("name", step.name))
    if step.rationale:
        parts.append(_render_tagged_block("rationale", step.rationale))
    if step.input is not None:
        parts.append(_render_tagged_block("input", step.input))
    if step.output is not None:
        parts.append(_render_tagged_block("output", step.output))
    if step.thought:
        parts.append(_render_tagged_block("thought", step.thought))
    parts.append("</TOOL_STEP>")
    return "\n".join(parts)


@render_function("shot")
def shot(
    *,
    title: str | None = None,
    context: LlmResponseLike | None = None,
    user: str | None = None,
    input: LlmResponseLike | None = None,
    tools: Sequence[ToolStep] = (),
    thought: str | None = None,
    output: LlmResponseLike,
) -> str:
    """Render a single **few-shot example** with optional context, tools, and thoughts.

    Args:
        title: Optional heading for the example.
        context: Optional context block.
        user: Optional user message (plain string is fine). When ``None``, the user block
            is omitted.
        input: Deprecated alias of ``model_input``; kept for backward compatibility.
        tools: Zero or more tool steps that were executed.
        thought: Optional chain-of-thought style comment (if you deliberately include it).
        output: The expected/target assistant output.

    Returns:
        A formatted example block suitable for inclusion in prompts.
    """
    main_parts: list[str] = []

    if title:
        main_parts.append(f"### {title}")

    if user is not None:
        main_parts.append(f"User: {user}")

    if context is not None:
        main_parts.append(_render_tagged_block("context", context))

    if input is not None:
        main_parts.append(_render_tagged_block("input", input))

    if tools:
        tool_steps_str = "\n".join(_render_tool_step(step) for step in tools)
        main_parts.append(f"<TOOL_CHAIN>\n{tool_steps_str}\n</TOOL_CHAIN>")

    if thought:
        main_parts.append(_render_tagged_block("thought", thought))

    main_parts.append(_render_tagged_block("output", output))
    return "\n\n".join(main_parts)
