from __future__ import annotations

from pragma_prompt.renderers.render_function import render_function


@render_function("code")
def code_block(source: str, lang: str | None = None) -> str:
    """Render a fenced Markdown code block.

    Args:
        source: Code text to include inside the fence.
        lang: Optional language tag (e.g., "python"). If omitted, a plain
            fenced block is emitted.

    Returns:
        Markdown fenced code block.

    Examples:
        >>> code_block("print('hi')", "python")
        '```python\\nprint(\\'hi\\')\\n```'
    """
    # Basic guard: if source already contains a closing fence, fall back to a longer fence
    fence = "```" + (lang or "")
    close = "```"
    if "```" in source:
        fence = "````" + (lang or "")
        close = "````"
    return f"{fence}\n{source}\n{close}"
