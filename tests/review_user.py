from __future__ import annotations

import prompt_craft_kit as pck

from tests.review import ReviewModule


render_model = ReviewModule.review_user.render_model

"""
# Evaluate the result against the expectation:
"""

with pck.section("test_case"):
    f"{render_model.test_case}"

with pck.section("test_input_params"):
    f"{render_model.input_params}"

with pck.section("test_expectation"):
    f"{render_model.expectation}"

with pck.section("test_output"):
    f"{render_model.output}"
