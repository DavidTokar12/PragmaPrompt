from __future__ import annotations

from pathlib import Path

import pytest

from pragma_prompt import Prompt
from pragma_prompt import PromptModule


def test_base_module_path() -> None:
    class TestModule(PromptModule[None]):
        review_user: Prompt[None, None]

    assert (
        TestModule.module_dir == Path(__file__).parent
    ), "The base module dir should be the files directory"


def test_initiated_with_file_path() -> None:
    class TestModule(PromptModule[None]):
        invalid_review_user: Prompt[None, None] = Prompt(filename="review_user")

    assert (
        TestModule.invalid_review_user._filename == "review_user.py"
    ), "The file name should be set as per the parameter"


def test_invalid_path_fails() -> None:
    with pytest.raises(FileNotFoundError):

        class TestModule(PromptModule[None]):
            not_existing_prompt: Prompt[None, None]


def test_other_params_set() -> None:

    # this is ok, just no error should be raised
    class TestModule(PromptModule[None]):
        other_param: int
