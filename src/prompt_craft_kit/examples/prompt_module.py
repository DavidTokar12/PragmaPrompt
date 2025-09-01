# from __future__ import annotations

# from pathlib import Path

# from prompt_craft_kit.prompt_api import Component
# from prompt_craft_kit.prompt_api import ComponentModule
# from prompt_craft_kit.prompt_api import Prompt
# from prompt_craft_kit.prompt_api import PromptModule


# class MyConstants: ...


# class MyContext: ...


# class MyRM: ...


# class CModule(ComponentModule[MyConstants]):
#     constants = MyConstants()
#     module_dir = Path(__file__).parent

#     section_meaning: Component = Component()
#     component: Component = Component()


# class PModule(PromptModule[MyConstants]):

#     constants = MyConstants()
#     module_dir = Path(__file__).parent

#     test_user: Prompt[MyContext, MyRM] = Prompt()
#     test_system: Prompt[MyContext, None] = Prompt()
