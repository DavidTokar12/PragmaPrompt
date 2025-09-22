from __future__ import annotations

from pragma_prompt.prompt_api import Component
from pragma_prompt.prompt_api import ComponentModule
from pragma_prompt.prompt_api import Prompt
from pragma_prompt.prompt_api import PromptModule
from pragma_prompt.renderers.render_functions.block import block
from pragma_prompt.renderers.render_functions.bullets import bullets
from pragma_prompt.renderers.render_functions.code_block import code_block
from pragma_prompt.renderers.render_functions.output_format import output_example
from pragma_prompt.renderers.render_functions.output_format import output_format
from pragma_prompt.renderers.render_functions.separator import separator
from pragma_prompt.renderers.render_functions.shot import ToolStep
from pragma_prompt.renderers.render_functions.shot import shot
from pragma_prompt.renderers.render_functions.table import table
from pragma_prompt.renderers.render_functions.warning import warning
from pragma_prompt.renderers.sections import section
from pragma_prompt.renderers.sections import section_end
from pragma_prompt.renderers.sections import section_start


__version__ = "1.0.0"

__all__ = [
    "Component",
    "ComponentModule",
    "Prompt",
    "PromptModule",
    "ToolStep",
    "block",
    "bullets",
    "code_block",
    "output_example",
    "output_format",
    "section",
    "section_end",
    "section_start",
    "separator",
    "shot",
    "table",
    "warning",
]

# TODO: Write README
# TODO: add 1 engaging examples
# TODO: make pipeline

# TODO: Redo all milo prompts with pragma prompt/fix add all urgent stuff
# TODO: Follow marketing strategy
