from __future__ import annotations

import pragma_prompt as pp

from examples.getting_started.prompts import MyPrompts


ctx = MyPrompts.daily_motivation.context
rm = MyPrompts.daily_motivation.render_model

"# Your job is to motivate the user."

if ctx.is_user_sad:
    "Go easy on the user, he is sad."
else:
    "Show him some tough love, he can handle it."

for i in range(3):
    f"Repetition {i+1}: Be concise and clear."

if ctx.user_is_new:
    "Explain the concepts simply."
else:
    "Assume the user is an expert."

with pp.section("user_data"):
    f"The users name is: {rm.user_id}"
