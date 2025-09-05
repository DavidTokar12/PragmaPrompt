from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pandas as pd
import pytest

from prompt_craft_kit import table
from prompt_craft_kit.runtime_context import session


MAPPINGS_DATA = [
    {"product_id": "A123", "name": "Wireless Mouse", "stock": 150},
    {"product_id": "B456", "name": "Mechanical Keyboard", "stock": 75},
]

SEQUENCE_DATA = [
    ("A123", "Wireless Mouse", 150),
    ("B456", "Mechanical Keyboard", 75),
]

CSV_STRING_DATA = (
    "product_id,name,stock\nA123,Wireless Mouse,150\nB456,Mechanical Keyboard,75"
)

DATAFRAME_DATA = pd.DataFrame(
    [
        {"product_id": "A123", "name": "Wireless Mouse", "stock": 150},
        {"product_id": "B456", "name": "Mechanical Keyboard", "stock": 75},
    ]
)


CASES = [
    (
        {"rows": MAPPINGS_DATA, "fmt": "pretty"},
        "This converts a list of dictionaries to a pretty-printed table. Verify that headers are inferred from keys and data is aligned in a readable table.",
        "mappings_to_pretty",
    ),
    (
        {"rows": MAPPINGS_DATA, "fmt": "csv"},
        "This converts a list of dictionaries to CSV format. Verify that headers are inferred from keys and the output is a valid, standard CSV string.",
        "mappings_to_csv",
    ),
    (
        {
            "rows": SEQUENCE_DATA,
            "headers": ["ID", "Product", "In Stock"],
            "fmt": "pretty",
        },
        "This converts a list of sequences to a pretty-printed table using explicit headers. Verify the provided headers are used and the data is aligned.",
        "sequence_to_pretty",
    ),
    (
        {"rows": SEQUENCE_DATA, "headers": ["ID", "Product", "In Stock"], "fmt": "csv"},
        "This converts a list of sequences to CSV format using explicit headers. Verify the provided headers are used and the output is a valid CSV string.",
        "sequence_to_csv",
    ),
    (
        {"rows": CSV_STRING_DATA, "fmt": "pretty"},
        "This parses a raw CSV string and formats it as a pretty table. Verify the headers are read from the first line and the data is correctly structured.",
        "csv_string_to_pretty",
    ),
    (
        {"rows": CSV_STRING_DATA, "fmt": "csv"},
        "This parses a raw CSV string and outputs it in standard CSV format. Verify the output is a valid, standard CSV string with a header row.",
        "csv_string_to_csv",
    ),
    (
        {"rows": DATAFRAME_DATA, "fmt": "pretty"},
        "This converts a pandas-like DataFrame into a pretty-printed table. Verify the headers are taken from the DataFrame's columns and the data is correctly rendered.",
        "dataframe_to_pretty",
    ),
    (
        {"rows": DATAFRAME_DATA, "fmt": "csv"},
        "This converts a pandas-like DataFrame into CSV format. Verify the headers are taken from the DataFrame's columns and the output is a valid CSV.",
        "dataframe_to_csv",
    ),
]


@pytest.mark.llm
@pytest.mark.parametrize("kwargs, description, case", CASES, ids=[c[-1] for c in CASES])
def test_table_cases(
    kwargs: dict[str, Any],
    description: str,
    case: str,
    llm_review: Callable,
    write_case_markdown: Callable,
    append_results: Callable,
) -> None:
    """
    Tests the table renderer with various data sources and output formats,
    relying on an LLM to evaluate the correctness of the output formatting.
    """
    with session():
        out = table(**kwargs)

    assert isinstance(out, str) and out

    loggable_kwargs = kwargs.copy()
    if isinstance(loggable_kwargs.get("rows"), pd.DataFrame):
        loggable_kwargs["rows"] = loggable_kwargs["rows"].to_dict("records")

    review = llm_review(
        renderer="table",
        case=case,
        input_params=loggable_kwargs,
        output=out,
        expectation=description,
    )

    md_file = write_case_markdown(
        renderer="table",
        case=case,
        input_params=loggable_kwargs,
        output=out,
        expectation=description,
        review=review,
    )

    append_results(file=md_file, review=review)
