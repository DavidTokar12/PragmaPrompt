from __future__ import annotations

from typing import Any


def pytest_addoption(parser: Any) -> None:  # pragma: no cover
    parser.addoption("--cov", action="store", default=None)
    parser.addoption("--cov-report", action="append", default=[])
    parser.addoption("--cov-fail-under", action="store", default=None)
