from __future__ import annotations

import pragma_prompt as pp

from pragma_prompt import block
from pragma_prompt import code_block
from pragma_prompt import table
from tests.includes.multi_renderer_prompt.module import MultiRendererPromptModule


# Get context and render model
ctx = MultiRendererPromptModule.multi_renderer_prompt.context
rm = MultiRendererPromptModule.multi_renderer_prompt.render_model

"""
This prompt demonstrates using multiple renderers with different types.
"""

# Pure string section (will be rendered with block)
"""
Welcome to the test prompt!
"""

# Use different renderers
with pp.section("table"):
    headers = ["Item", "Value"]
    rows = [(item, "✓") for item in ctx.items]
    table(headers=headers, rows=rows)

with pp.section("code"):
    code = f"""def process_items():
    # Process items for {ctx.user_id}
    items = {ctx.items!r}
    return [item.upper() for item in items]"""
    code_block(code, lang="python")

with pp.section("block"):
    block(f"Template: {rm.template_name}")
    block(f"Timestamp: {rm.timestamp}")
