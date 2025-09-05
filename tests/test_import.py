from __future__ import annotations

import pytest

from prompt_craft_kit.exceptions import LoaderError
from tests.includes.circular_import_fail_1.module import CircularImportModule
from tests.includes.including_prompt_fail.module import (
    ImportPromptModule as ImportPromptModule2,
)
from tests.includes.rendering_components_and_prompts.module import (
    ImportPromptModule as ImportPromptModule1,
)


def test_circular_import_1_fail():

    with pytest.raises(LoaderError):
        CircularImportModule.component_1.render()

    with pytest.raises(LoaderError):
        CircularImportModule.component_2.render()


def test_import():

    prompt = ImportPromptModule1.prompt_1.render()

    assert "prompt 1" in prompt
    assert "component 1" in prompt
    assert "component 2" in prompt


def test_importing_prompt_fails():

    with pytest.raises(LoaderError):
        ImportPromptModule2.prompt_1.render()


# test for invalid section opening/closing

# test for loading every component and rendering it

# multi threaded tests
