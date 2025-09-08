from __future__ import annotations

from prompt_craft_kit.prompt_api import Component
from prompt_craft_kit.prompt_api import ComponentModule
from prompt_craft_kit.prompt_api import Prompt
from prompt_craft_kit.prompt_api import PromptModule
from prompt_craft_kit.renderers.render_functions.block import block
from prompt_craft_kit.renderers.render_functions.bullets import bullets
from prompt_craft_kit.renderers.render_functions.code_block import code_block
from prompt_craft_kit.renderers.render_functions.output_format import output_example
from prompt_craft_kit.renderers.render_functions.output_format import output_format
from prompt_craft_kit.renderers.render_functions.separator import separator
from prompt_craft_kit.renderers.render_functions.shot import ToolStep
from prompt_craft_kit.renderers.render_functions.shot import shot
from prompt_craft_kit.renderers.render_functions.table import table
from prompt_craft_kit.renderers.render_functions.warning import warning
from prompt_craft_kit.renderers.sections import section
from prompt_craft_kit.renderers.sections import section_end
from prompt_craft_kit.renderers.sections import section_start


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


# TODO: Make a 'test generation' function that will return the prompt with default context/constants/render models

# TODO: somehow generate a hash for a prompt

# TODO: add output format renderer

# TODO: add 3 engaging examples

# TODO: lint with pyright

# TODO: Write docs

# TODO: make correct pipeline

# TODO: Redo all milo prompts with prompt craft kit/fix add all urgent stuff.

# TODO: Do marketing on reddit/AI tinkerers/LinkedIn.

# TODO: Research new ideas that could be added to this.
