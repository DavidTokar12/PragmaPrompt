from __future__ import annotations

from dataclasses import dataclass

from prompt_craft_kit import Component
from prompt_craft_kit import ComponentModule
from prompt_craft_kit import Prompt
from prompt_craft_kit import PromptModule


@dataclass
class RedditRenderModel:
    subreddit: str
    theme: str
    audience: str


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
    """
    Reusable building blocks for the Reddit agent.
    Each attribute corresponds to a file in this directory.
    """

    platform_rules: Component
    safety_disclaimer: Component


class RedditAgent(PromptModule[None]):
    """
    Prompts for authoring threads and generating replies.
    """

    write_post: Prompt[None, RedditRenderModel]
    write_replies: Prompt[None, RedditRenderModel]


if __name__ == "__main__":
    with open("xd.txt", mode="w") as f:
        rm = RedditRenderModel(subreddit="anal", theme="porn", audience="gooners")
        f.write(RedditAgent.write_post.render(render_model=rm))
