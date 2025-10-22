from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pragma_prompt as pp


class MyConstants:
    default_tone = "helpful"
    max_length = 1000


@dataclass
class MyRenderModel:
    user_id: str = "123"


@dataclass
class MyContext:
    text_to_summarize: str = "This is some text to summarize..."
    is_user_sad: bool = False
    user_is_new: bool = False


class MyComponents(pp.ComponentModule[None]):
    module_dir = Path(__file__).parent / "component_files"

    output_format: pp.Component[MyRenderModel] = pp.Component()


class MyPrompts(pp.PromptModule[MyConstants]):
    module_dir = Path(__file__).parent / "prompt_files"
    constants = MyConstants()

    daily_motivation: pp.Prompt[MyContext, MyRenderModel] = pp.Prompt(
        "daily_motivation.py"
    )
    summarize: pp.Prompt[MyContext, MyRenderModel] = pp.Prompt("summarize.py")


if __name__ == "__main__":
    MyPrompts.daily_motivation.render(context=MyContext(), render_model=MyRenderModel())

    MyPrompts.summarize.render(context=MyContext(), render_model=MyRenderModel())
