from __future__ import annotations

from examples.getting_started.prompts import MyComponents
from examples.getting_started.prompts import MyPrompts


ctx = MyPrompts.summarize.context
rm = MyPrompts.summarize.render_model
constants = MyPrompts.constants

f"Your tone should be {constants.default_tone}."
f"Summarize the following text for user {rm.user_id}:"
f"{ctx.text_to_summarize}"

MyComponents.output_format.render()
