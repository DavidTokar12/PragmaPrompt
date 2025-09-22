# PragmaPrompt

## logo -> we need to make one first of crouse

## badges -> ones that are easy, but look nice

## A toolkit for building, managing, and composing hierarchical prompts as Python code.

* **Prompts as real Python (lint, test, type, ship).**
  Get linters, formatters, type checking, unit tests, imports, and refactors—the whole Python toolchain applied to your prompts.
* **Compose & standardize.**
  Nest prompts inside prompts, reuse modules, and snap in built-in renderers (`warning`, `bullets`, `output_format`, `section`, …) for consistent, maintainable, and token-efficient outputs.
* **Context-aware rendering.**
  Use plain Python control flow (ifs/loops/guards) to generate the right prompt for each situation—no more nasty string templating.

#

```
import pragma_prompt as pp
from my_module import MyModule

ctx = MyModule.my_prompt.context
rm = MyModule.my_prompt.render_model

"# Your job is to motivate the user."

if ctx.is_user_sad:
    "Go easy on the user, he is sad."
else:
    "Show him some though love, he can handle it."

with pck.section("user_data"):
    f"The users name is: {rm.user_name}"
```

Result:
```
# Your job is to motivate the user.
Go easy on the user, he is sad.
<user_data>
The users name is: John
</user_data>
```


# docs

# Short explanation how the prompts ar built, and what to understand

here I want to basically metnion that this is true python code so:

for _ in range(10):
    "Hello"

will render 'Hello' 10 times.

# explain how to instantiate prompt modules

# explain how to import components within prompts

# best practices

# reference to all renderers
