# PragmaPrompt: A toolkit for building, managing, and composing hierarchical prompts as Python code.


![License](https://img.shields.io/github/license/DavidTokar12/PragmaPrompt)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Type hints](https://img.shields.io/badge/types-PEP%20561-informational)
[![codecov](https://codecov.io/gh/DavidTokar12/PragmaPrompt/branch/main/graph/badge.svg)](https://codecov.io/gh/DavidTokar12/PragmaPrompt)

---

* **Prompts as real Python (lint, test, type, ship).**
  Get linters, formatters, type checking, unit tests, imports, and refactors—the whole Python toolchain applied to your prompts.
* **Compose & standardize.**
  Nest prompts inside prompts, reuse modules, and snap in built-in renderers (`warning`, `bullets`, `output_example`, `section`, …) for consistent, maintainable, and token-efficient outputs.
* **Context-aware rendering.**
  Use plain Python control flow (ifs/loops/guards) to generate the right prompt for each situation—no more nasty string templating.

## Installation

```bash
pip install pragma-prompt
```

#

```python
import pragma_prompt as pp

from examples.getting_started.prompts import MyPrompts

# typed context and render model
ctx = MyPrompts.daily_motivation.context
rm = MyPrompts.daily_motivation.render_model

"# Your job is to motivate the user."

if ctx.is_user_sad:
    "Go easy on the user, he is sad."
else:
    "Show him some tough love, he can handle it."

with pp.section("user_data"):
    f"The users name is: {rm.user_id}"
```

Result:
```
# Your job is to motivate the user.
Show him some tough love, he can handle it.
<USER_DATA>
The users name is: 123
</USER_DATA>
```


# How It Works

At its core, PragmaPrompt executes your prompts as Python files. This means you can use the full power of Python—loops, conditionals, functions, and imports—to dynamically construct your prompts. Any bare string literal is automatically captured and rendered as a normalized text block.

This approach turns prompt engineering into a familiar software development process. You can lint, test, and version your prompts just like any other code.

```python
for i in range(3):
    f"Repetition {i+1}: Be concise and clear."
```

This will render:
```
Repetition 1: Be concise and clear.
Repetition 2: Be concise and clear.
Repetition 3: Be concise and clear.
```

## Defining and Using Prompts

To get started, you define `PromptModule` and `ComponentModule` classes. These act as namespaces that organize your prompts and reusable components.

### 1. Create a Prompt Module

A `PromptModule` is a class that groups related prompts and provides them with shared constants.

```python
# in examples/getting_started/prompts.py
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

    output_format: pp.Component[MyRenderModel]


class MyPrompts(pp.PromptModule[MyConstants]):
    module_dir = Path(__file__).parent / "prompt_files"
    constants = MyConstants()

    daily_motivation: pp.Prompt[MyContext, MyRenderModel]
    summarize: pp.Prompt[MyContext, MyRenderModel]
```

### 2. Write Your Prompt File

Your prompt file is a standard Python file. You can access the prompt's `context` and `render_model` using a tuple assignment, and the module's `constants` via `MyPrompts.constants`.

```python
# in examples/getting_started/prompt_files/summarize.py
from examples.getting_started.prompts import MyComponents
from examples.getting_started.prompts import MyPrompts

# Get typed handles to context, render_model and constants inside an active session
ctx = MyPrompts.summarize.context
rm = MyPrompts.summarize.render_model
constants = MyPrompts.constants

f"Your tone should be {constants.default_tone}."
f"Summarize the following text for user {rm.user_id}:"
f"{ctx.text_to_summarize}"

# render reusable components 
MyComponents.output_format.render()
```

Result:
```
Your tone should be helpful.
Summarize the following text for user 123:
This is some text to summarize...
<NOTICE>
You must respond in JSON.
</NOTICE>
{
  "summary": "...",
  "tags": [
  ]
}
```


### 3. Render the Prompt

To render the prompt, you call the `.render()` method on the prompt object, passing in the required `context` and `render_model` data.

```python
# The data you want to inject into the prompt
@dataclass
class MyRenderModel:
    user_id: str = "123"

@dataclass
class MyContext:
    text_to_summarize: str = "This is some text to summarize..."
    is_user_sad: bool = False
    user_is_new: bool = False

if __name__ == "__main__":
    MyPrompts.daily_motivation.render(
            context=MyContext(),
            render_model=MyRenderModel()
        )
```

> ⚠️ When you call `.render(...)` from module scope, guard it with `if __name__ == "__main__":` to avoid importing the same module recursively during rendering.


## Composing Prompts with Components

`Component`s are reusable snippets that can be imported into your prompts. They are ideal for standardizing instructions, formats, or examples.

### 1. Create a Component Module

Similar to a `PromptModule`, a `ComponentModule` organizes your reusable components.

```python
# in my_app/components.py
from pathlib import Path
import pragma_prompt as pp

class MyComponents(pp.ComponentModule):
    module_dir = Path(__file__).parent / "component_files"
    
    # This component will be loaded from 'output_format.py'
    output_format: pp.Component[MyRenderModel]
```

### 2. Write Your Component File

Component files are simpler than prompt files. They can access shared `constants` and the active `render_model`, but they do not receive a prompt `context`.

```python
import pragma_prompt as pp

pp.warning("You must respond in JSON.")
pp.output_example({"summary": "...", "tags": []})
```

### 3. Import and Use the Component in a Prompt

You can import component modules directly into your prompt files and call the component's `.render()` method to insert its content.

```python
from examples.getting_started.prompts import MyComponents
from examples.getting_started.prompts import MyPrompts

ctx = MyPrompts.summarize.context
rm = MyPrompts.summarize.render_model
constants = MyPrompts.constants

f"Your tone should be {constants.default_tone}."
f"Summarize the following text for user {rm.user_id}:"
f"{ctx.text_to_summarize}"

# Render the component to include its content
MyComponents.output_format.render()
```

When `MyPrompts.summarize` is rendered, the content of the `output_format` component will be included directly in the final output. This allows you to build complex prompts from standardized, reusable parts.

-----

# Renderers

## `block(...)` — normalized text block

**Signature:** `pp.block(content: str) -> str`
**What it does:** Dedents and strips a string so it drops cleanly into your prompt (no leading indentation, no extra surrounding whitespace).
**When to use:** Any freeform text chunk (instructions, short paragraphs).

**Implicit call:** Bare string literals inside a prompt body are treated as `block(...)` automatically.

```python
# implicit
"Summarize the discussion in 3 sentences."

# explicit (equivalent)
pp.block("Summarize the discussion in 3 sentences.")
````

**Returns:** normalized string (dedented + stripped).

-----

## `bullets(...)` — compact bullet list

**Signatures:**

```python
pp.bullets(items: Mapping[str, Any]) -> str
pp.bullets(items: Sequence[tuple[str, Any]]) -> str
pp.bullets(items: Sequence[Any]) -> str
```

**What it does:** Renders a tight list with `-` markers.

  * Mapping → `- key: value` (order follows the mapping’s iteration order)
  * Sequence of `(key, value)` → `- key: value`
  * Sequence of values → `- value`

<!-- end list -->

```python
pp.bullets({'role': 'analyst', 'tone': 'concise'})
# - role: analyst
# - tone: concise
pp.bullets([('role', 'analyst'), ('tone', 'concise')])
# - role: analyst
# - tone: concise
pp.bullets(['Discussion', 'Serious', 'Debate'])
# - Discussion
# - Serious
# - Debate
```

**Returns:** newline-joined bullet string.

-----

## `code_block(...)` — fenced Markdown code

**Signature:** `pp.code_block(source: str, lang: str | None = None) -> str`
**What it does:** Emits a fenced Markdown code block. If `lang` is set, it tags the fence for syntax highlighting. If the `source` already contains \`\`\` fences, it automatically switches to \`\`\`\` fences.

````python
pp.code_block("print('hi')", 'python')
# ```python
# print('hi')
# ```
````

**Returns:** fenced Markdown code block as a string.

-----

## `output_example(...)` — pretty JSON with inline `// comments`

**Signature**

```python
pp.output_example(
    data: LlmResponseLike,
    comments: CommentTreeOrStr | None = None,
) -> str
```

**What it does**
Renders **pretty JSON** and lets you attach inline `// comments` to any node:

  * **Primitives:** comment appears on the same line as the value.
  * **Objects & arrays:** comment appears on the **closing** brace/bracket line of that node.

**Comments syntax (simple & strict)**

  * `comments` may be:

      * a **root string** → comment on the whole value, or

      * a **nested mapping** that mirrors your data shape:

          * At any object/array node you can EITHER:
              * provide a **single string** (comment on that whole node), **or**
              * provide a **mapping of subkeys** (per-field/per-index comments),
              * **not both** at the same node.
          * Arrays use **numeric string indices** (`"0"`, `"1"`, …).

  * All comment keys/indices must exist in `data`; unknown keys raise `ValueError`.

**Examples**

Root comment (whole object):

```python
pp.output_example({'a': 1}, comments='Overall guidance')
# {
#   "a": 1
# } // Overall guidance
```

Object-level comment:

```python
data = {'user': {'name': 'Ada', 'age': 30}, 'count': 1}
pp.output_example(data, comments={'user': 'User metadata'})
# {
#   "count": 1,
#   "user": {
#     "age": 30,
#     "name": "Ada"
#   } // User metadata
# }
```

Per-field comments:

```python
schema = {'sentiment': 'positive|neutral|negative', 'summary': '', 'tags': []}
pp.output_example(
    schema,
    comments={'summary': '1–2 concise sentences', 'sentiment': 'pick exactly one', 'tags': '0–5 lowercase topics'},
)
# {
#   "sentiment": "positive|neutral|negative", // pick exactly one
#   "summary": "", // 1–2 concise sentences
#   "tags": [
#   ] // 0–5 lowercase topics
# }
```

Nested and array index comments:

```python
data = {'user': {'name': 'Ada', 'roles': ['admin', 'ops']}, 'count': 2}
pp.output_example(
    data,
    comments={'user': {'name': 'Display name', 'roles': {'0': 'Primary role'}}, 'count': 'Number of items'},
)
# {
#   "count": 2, // Number of items
#   "user": {
#     "name": "Ada", // Display name
#     "roles": [
#       "admin", // Primary role
#       "ops"
#     ]
#   }
# }
```

**Returns**
A string containing pretty JSON with inline `// comments`. The JSON structure is valid if you strip the `// …` parts.

## `separator(...)` — visual divider (optional title)

**Signature**

```python
pp.separator(
    title: str | None = None,
    *,
    char: str = "-",
    width: int = 80,
) -> str
```

**What it does**
Draws a clean ASCII divider line. With a `title`, it centers the text and pads both sides.

**Rules & defaults**

  * `width` defaults to **80**.
  * `char` must be a single visible character; defaults to `"-"`.
  * When `title` is provided, emits a **single centered line**.

**Examples**

```python
pp.separator()
# --------------------------------------------------------------------------------
pp.separator(char='=', width=10)
# ==========
pp.separator(title='CONTEXT')
# ----------------------------------- CONTEXT ------------------------------------
pp.separator(title='X', char='*', width=9)
# *** X ***
pp.separator(width=2)
# --
```

**Returns**
A single string.

-----

## `shot(...)` — a structured, single example (prompt + reasoning + tools + output)

**Signature**

```python
pp.shot(
    *,
    title: str | None = None,
    context: LlmResponseLike | None = None,
    user: str | None = None,
    input: LlmResponseLike | None = None,
    tools: Sequence[ToolStep] = (),
    thought: str | None = None,
    output: LlmResponseLike,
) -> str
```

**What it does**
Emits a compact, **readable “example shot”**: the user prompt, optional context/input, an optional **tool-call chain**, optional intermediate **thought**, and the final **output**. Great for few-shot prompting and rich examples that still parse well for LLMs.

**Block order (when present)**

1.  `title` (as a one-line heading)
2.  **User** (skipped when no user message is provided)
3.  **Context** (pretty-printed, deterministic JSON from dict/dataclass/Pydantic)
4.  **Input** (pretty JSON)
5.  **Tool call chain** (each step: name, rationale, input, output, optional thought)
6.  **Thought**
7.  **Output** (pretty JSON or string)

**Tool steps**

```python
ToolStep(
    name: str
    rationale: str | None = None
    input: LlmResponseLike | None = None
    output: LlmResponseLike | None = None
    thought: str | None = None
)
```

**Examples**

Minimal:

```python
pp.shot(
    user="What is the capital of Switzerland?",
    output="Bern",
)
# User: What is the capital of Switzerland?
# Output: Bern
```

Context + input:

```python
class UserProfile(BaseModel):
    username: str
    expertise_level: str = Field(description="User's familiarity with the subject")
pp.shot(
    user="What's the outlook for this company?",
    context=UserProfile(username="investor_bob", expertise_level="beginner"),
    input={"company_ticker": "TCORP", "timeframe": "6 months"},
    output="The outlook is positive, but volatile.",
)
# User: What's the outlook for this company?
# Context:
# {
#   "expertise_level": "beginner",
#   "username": "investor_bob"
# }
# Input:
# {
#   "company_ticker": "TCORP",
#   "timeframe": "6 months"
# }
# Output: The outlook is positive, but volatile.
```

With chain-of-thought note:

```python
pp.shot(
    user="Write a short poem about the moon.",
    thought="Plan: evoke night/light imagery; 3 short stanzas.",
    output="Silver orb in velvet night...",
)
# User: Write a short poem about the moon.
# Thought: Plan: evoke night/light imagery; 3 short stanzas.
# Output: Silver orb in velvet night...
```

With a single tool call:

```python
pp.shot(
    user="Search for today's top finance news.",
    tools=[
        ToolStep(
            name="web_search",
            rationale="User asked for current news.",
            input={"query": "top finance news today", "domain": "finance"},
            output={"url": "[news.com/1](https://news.com/1)", "title": "Market Hits New High", "snippet": "..."},
        )
    ],
    output={"summary": "The market reached a new high today, driven by tech stocks."},
)
# User: Search for today's top finance news.
# Tool (web_search): User asked for current news.
#   Input:
#   {
#     "domain": "finance",
#     "query": "top finance news today"
#   }
#   Output:
#   {
#     "snippet": "...",
#     "title": "Market Hits New High",
#     "url": "[news.com/1](https://news.com/1)"
#   }
# Output:
# {
#   "summary": "The market reached a new high today, driven by tech stocks."
# }
```

“Kitchen sink” (title, context, multiple tools, thought, structured output):

```python
pp.shot(
    title="Example: Research and Summarize Financial Report",
    user="Find the latest quarterly earnings for 'TechCorp' and summarize key takeaways.",
    context={"username": "analyst_jane", "expertise_level": "expert"},
    tools=[
        ToolStep(
            name="web_search",
            rationale="Find the official press release.",
            input={"query": "TechCorp latest quarterly earnings report"},
            output={"url": "[investors.techcorp.com/q3-2025-earnings](https://investors.techcorp.com/q3-2025-earnings)", "title": "TechCorp Reports Q3 2025", "snippet": "..."},
            thought="First result is the official source."
        ),
        ToolStep(
            name="summarize_document",
            rationale="Summarize key points.",
            input={"url": "[investors.techcorp.com/q3-2025-earnings](https://investors.techcorp.com/q3-2025-earnings)"},
            output={"summary": "Strong earnings from cloud.", "takeaways": ["Revenue hit $50B."]},
        ),
    ],
    thought="Tool chain complete; formatting final answer.",
    output={
        "summary": "TechCorp reported record revenue of $50B in Q3 2025, driven by cloud.",
        "key_takeaways": ["Record revenue", "Cloud +25% YoY"],
        "confidence_score": 0.95,
    },
)
# Example: Research and Summarize Financial Report
# ------------------------------------------------
# User: Find the latest quarterly earnings for 'TechCorp' and summarize key takeaways.
# Context:
# {
#   "expertise_level": "expert",
#   "username": "analyst_jane"
# }
# Tool (web_search): Find the official press release.
#   Thought: First result is the official source.
#   Input:
#   {
#     "query": "TechCorp latest quarterly earnings report"
#   }
#   Output:
#   {
#     "snippet": "...",
#     "title": "TechCorp Reports Q3 2025",
#     "url": "[investors.techcorp.com/q3-2025-earnings](https://investors.techcorp.com/q3-2025-earnings)"
#   }
# Tool (summarize_document): Summarize key points.
#   Input:
#   {
#     "url": "[investors.techcorp.com/q3-2025-earnings](https://investors.techcorp.com/q3-2025-earnings)"
#   }
#   Output:
#   {
#     "summary": "Strong earnings from cloud.",
#     "takeaways": [
#       "Revenue hit $50B."
#     ]
#   }
# Thought: Tool chain complete; formatting final answer.
# Output:
# {
#   "confidence_score": 0.95,
#   "key_takeaways": [
#     "Record revenue",
#     "Cloud +25% YoY"
#   ],
#   "summary": "TechCorp reported record revenue of $50B in Q3 2025, driven by cloud."
# }
```

**Returns**
A single string with all sections rendered in a stable, LLM-friendly layout.

## `table(...)` — render small tables from dicts/lists/CSV/DataFrames

**Overloads**

```python
pp.table(
    rows: RowsLike,
    headers: Sequence[str] | None = None,
    fmt: TableFormat = "csv",
) -> str
```

**What it does**
Turns your data into a compact table. Accepts:

  * **Rows of mappings** (`Sequence[Mapping[str, Any]]`)
  * **Rows of sequences** (`Sequence[Sequence[Any]]`)
  * **Pandas-like DataFrame** (`.columns` and `.itertuples(index=False, name=None)`)
  * **CSV** (pass a string of CSV text, or a `Path/PathLike` to read a file)

**Headers & normalization**

  * If `headers=None`:

      * **Mappings:** union of keys in iteration order (first row’s order, then unseen keys).
      * **Sequences:** headers auto-generated: `col1`, `col2`, …
      * **DataFrame:** uses `df.columns`.
      * **CSV text/path:** uses first row as headers.

  * If `headers` provided, rows are **padded/truncated** to that width.

**Formats**

  * `fmt="pretty"` → uses **prettytable** (must be installed).
  * `fmt="csv"` → emits CSV text (via `csv.writer`).
  * Raises `RuntimeError` if `fmt="pretty"` and `prettytable` is missing; `ValueError` if `fmt` is not `"pretty"` or `"csv"`.

**Examples**

Mappings (pretty):

```python
rows = [{'name': 'Ada', 'role': 'admin'}, {'name': 'Bob'}]
pp.table(rows)
# name,role
# Ada,admin
# Bob,
```

Sequences with explicit headers (csv):

```python
rows = [
    ['Ada', 'admin', 5],
    ['Bob', 'viewer', 2],
]
pp.table(rows, headers=['name', 'role'], fmt='csv')
# name,role
# Ada,admin
# Bob,viewer
```

CSV text in, pretty out:

```python
csv_text = 'name,score\nAda,10\nBob,8\n'
pp.table(csv_text, fmt='pretty')
# +------+-------+
# | name | score |
# +------+-------+
# | Ada  | 10    |
# | Bob  | 8     |
# +------+-------+
```

DataFrame-like:

```python
class MiniDf:
    columns = ['name', 'v']
    def itertuples(self, *, index: bool, name: None):
        yield ('Ada', 1)
        yield ('Bob', 2)
pp.table(MiniDf(), fmt='csv')
# name,v
# Ada,1
# Bob,2
```

**Returns**
A single string containing the rendered table.

-----

## `warning(...)` — tagged warning blocks (3 severity levels)

**Overloads**

```python
pp.warning(body: str,          *, level: Literal[1,2,3] = 1, title: str | None = None) -> str
pp.warning(body: LlmResponseLike, *, level: Literal[1,2,3] = 1, title: str | None = None) -> str
```

**What it does**
Emits a warning using **XML-style tags**, with escalating emphasis by `level`.

**Levels**

  * `level=1` → `<NOTICE>…</NOTICE>`
  * `level=2` → `<WARNING>…</WARNING>`
  * `level=3` → `<CONSTRAINT>…</CONSTRAINT>`

**Args**

  * `body`: string or any `LlmResponseLike` (normalized via `to_display_block`).
  * `title`: optional text prepended to the body as `"Title: ..."` inside the tag.
  * Raises `ValueError` if `level` not in `{1,2,3}`.

**Examples**

Basic:

```python
pp.warning('Be careful with rate limits.')
# <NOTICE>
# Be careful with rate limits.
# </NOTICE>
```

With a title and level 2:

```python
pp.warning('Requests must be idempotent.', level=2, title='API')
# <WARNING>
# API: Requests must be idempotent.
# </WARNING>
```

Critical (level 3) with structured body:

```python
pp.warning({'do': 'return JSON only', 'dont': 'write prose'}, level=3)
# <CONSTRAINT>
# {
#   "do": "return JSON only",
#   "dont": "write prose"
# }
# </CONSTRAINT>
```

**Returns**
A single string with the formatted warning block.

-----

## Notes & Limitations

  - ⚠️ Compare enums with `==`/`!=` instead of `is`/`is not`. PragmaPrompt recompiles prompt files in a fresh module during each render, so enum objects do not preserve identity across runs.