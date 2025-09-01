from __future__ import annotations

from collections.abc import Mapping
from collections.abc import Sequence
from typing import Any
from typing import overload

from prompt_craft_kit.renderers.render_function import render_function
from prompt_craft_kit.renderers.renderers import Renderers
from prompt_craft_kit.renderers.utils import to_display_block


@overload
def kv(items: Mapping[str, Any]) -> str: ...
@overload
def kv(items: Sequence[tuple[str, Any]]) -> str: ...


@render_function(Renderers.KV)
def kv(items: Mapping[str, Any] | Sequence[tuple[str, Any]]) -> str:
    """
    Compact key-value rendering (Markdown definition-list-ish).
      kv({"role": "analyst", "tone": "concise"})
    """
    pairs: Sequence[tuple[str, Any]]
    pairs = list(items.items()) if isinstance(items, Mapping) else list(items)

    lines: list[str] = []
    for k, v in pairs:
        lines.append(f"- {k}: {to_display_block(v)}")
    return "\n".join(lines)
