from __future__ import annotations

from tests.includes.circular_import_fail_1.module import CircularImportModule


"""
component 2
"""

CircularImportModule.component_1.render()
