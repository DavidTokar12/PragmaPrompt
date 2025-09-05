from __future__ import annotations

from pathlib import Path

import pytest

from prompt_craft_kit import Prompt
from prompt_craft_kit import PromptModule


def test_base_module_path():
    class TestModule(PromptModule):
        review_user: Prompt

    assert (
        TestModule.module_dir == Path(__file__).parent
    ), "The base module dir should be the files directory"


def test_initiated_with_file_path():
    class TestModule(PromptModule):
        invalid_review_user: Prompt = Prompt(filename="review_user")

    assert (
        TestModule.invalid_review_user._filename == "review_user.py"
    ), "The file name should be set as per the parameter"


def test_invalid_path_fails():
    with pytest.raises(FileNotFoundError):

        class TestModule(PromptModule):
            not_existing_prompt: Prompt


def test_other_params_set():

    # this is ok, just no error should be raised
    class TestModule(PromptModule):
        other_param: int
