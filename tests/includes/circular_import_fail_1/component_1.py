from __future__ import annotations

from tests.includes.circular_import_fail_1.module import CircularImportModule


"""
component 1
"""

CircularImportModule.component_2.render()
