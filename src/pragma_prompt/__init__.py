from __future__ import annotations

from pathlib import Path

from pragma_prompt.prompt_api import Component
from pragma_prompt.prompt_api import ComponentModule
from pragma_prompt.prompt_api import Prompt
from pragma_prompt.prompt_api import PromptModule
from pragma_prompt.renderers.render_functions.block import block
from pragma_prompt.renderers.render_functions.bullets import bullets
from pragma_prompt.renderers.render_functions.code_block import code_block
from pragma_prompt.renderers.render_functions.output_format import output_example
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
    "section",
    "section_end",
    "section_start",
    "separator",
    "shot",
    "table",
    "write_readme",
    "warning",
]

# TODO: Fix separator -> remove boxed, token efficient
_README_TEMPLATE = """# Pragma Prompt

Pragma Prompt helps teams build reproducible, prompt-driven workflows using
declarative components and pluggable renderers. It ships with batteries for
structured prompt composition, rich formatting, and ergonomic pipeline reuse.

## Installation

```bash
pip install pragma-prompt
```

## Quick start

```python
from pragma_prompt import Prompt, section, block

prompt = Prompt("MyPrompt", steps=[section("Plan"), block("Do the work.")])
print(prompt.render())
```

## Documentation

- Explore components in `pragma_prompt.prompt_api`
- Mix and match renderers from `pragma_prompt.renderers`

"""


def write_readme(destination: str | Path = "README.md", *, overwrite: bool = False) -> Path:
    """Write a pre-populated README.md and return the target path."""

    target = Path(destination)
    if target.exists() and not overwrite:
        return target

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_README_TEMPLATE, encoding="utf-8")
    return target

# TODO: add 1 engaging example
# TODO: make pipeline
# TODO: Redo all milo prompts with pragma prompt/fix add all urgent stuff
# TODO: Follow marketing strategy
