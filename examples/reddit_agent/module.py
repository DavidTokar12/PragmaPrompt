from __future__ import annotations

from dataclasses import dataclass

from pragma_prompt import Component
from pragma_prompt import ComponentModule
from pragma_prompt import Prompt
from pragma_prompt import PromptModule


@dataclass
class RedditRenderModel:
    subreddit: str
    theme: str
    audience: str
    target_user: str = ""
    bait_comment: str = ""
    gaslight_hook: str = ""


@dataclass
class RedditPostOutput:
    title: str
    body_markdown: str
    flair: str | None


@dataclass
class RedditReplyOutput:
    reply_markdown: str
    mood: str
    safety_notes: list[str]


class RedditComponents(ComponentModule[None]):
    brand_voice: Component
    platform_rules: Component
    safety_disclaimer: Component


class RedditAgent(PromptModule[None]):
    write_post: Prompt[None, RedditRenderModel]
    write_replies: Prompt[None, RedditRenderModel]


if __name__ == "__main__":
    with open("output.txt", mode="w") as f:
        rm = RedditRenderModel(
            subreddit="csMajors", theme="vibe coding", audience="new grads"
        )
        f.write(RedditAgent.write_post.render(render_model=rm))
