from __future__ import annotations

import csv

from collections.abc import Iterable
from collections.abc import Mapping
from collections.abc import Sequence
from io import StringIO
from os import PathLike
from pathlib import Path
from typing import Any
from typing import Literal
from typing import Protocol
from typing import cast
from typing import overload

from pragma_prompt.renderers.render_function import render_function


class _PandasLikeDataFrame(Protocol):
    @property
    def columns(self) -> Sequence[str]: ...
    def itertuples(self, *, index: bool, name: None) -> Iterable[tuple[Any, ...]]: ...


TableFormat = Literal["pretty", "csv"]

RowsMapping = Sequence[Mapping[str, Any]]
RowsSequence = Sequence[Sequence[Any]]
CsvLike = str | Path | PathLike[str]
DfLike = _PandasLikeDataFrame
RowsLike = RowsMapping | RowsSequence | CsvLike | DfLike


def _is_dataframe(obj: Any) -> bool:
    return hasattr(obj, "itertuples") and hasattr(obj, "columns")


def _normalize_from_mappings(
    mrows: RowsMapping, headers: Sequence[str] | None
) -> tuple[list[str], list[list[Any]]]:
    if not mrows:
        return (list(headers) if headers else []), []
    if headers is None:
        first_keys = list(mrows[0].keys())
        seen = set(first_keys)
        rest: list[str] = []
        for r in mrows[1:]:
            for k in r:
                if k not in seen:
                    seen.add(k)
                    rest.append(k)
        hdrs = first_keys + rest
    else:
        hdrs = list(headers)
    matrix = [[row.get(h, "") for h in hdrs] for row in mrows]
    return hdrs, matrix


def _normalize_from_sequences(
    srows: RowsSequence, headers: Sequence[str] | None
) -> tuple[list[str], list[list[Any]]]:
    matrix = [list(r) for r in srows]
    if not matrix:
        return (list(headers) if headers else []), []
    if headers is None:
        hdrs = [f"col{i+1}" for i in range(len(matrix[0]))]
    else:
        hdrs = list(headers)
        width = len(hdrs)
        matrix = [row[:width] + [""] * max(0, width - len(row)) for row in matrix]
    return hdrs, matrix


def _normalize_from_dataframe(
    df: DfLike, headers: Sequence[str] | None
) -> tuple[list[str], list[list[Any]]]:
    cols = list(df.columns)
    matrix = [list(t) for t in df.itertuples(index=False, name=None)]
    if headers is not None:
        hdrs = list(headers)
        width = len(hdrs)
        matrix = [row[:width] + [""] * max(0, width - len(row)) for row in matrix]
    else:
        hdrs = cols
    return hdrs, matrix


def _normalize_from_csv_src(
    src: CsvLike, headers: Sequence[str] | None
) -> tuple[list[str], list[list[Any]]]:
    # Runtime isinstance checks must use tuples of types
    if isinstance(src, Path | PathLike):
        text = Path(src).read_text(encoding="utf-8")
    else:
        text = src
    reader = csv.reader(StringIO(text))
    rows = list(reader)
    if not rows:
        return (list(headers) if headers else []), []
    if headers is None:
        hdrs = [str(h) for h in rows[0]]
        data = rows[1:]
    else:
        hdrs = list(headers)
        data = rows
    width = len(hdrs)
    matrix = [r[:width] + [""] * max(0, width - len(r)) for r in data]
    return hdrs, matrix


def _normalize(
    rows: RowsLike, headers: Sequence[str] | None
) -> tuple[list[str], list[list[Any]]]:
    if _is_dataframe(rows):
        return _normalize_from_dataframe(cast("DfLike", rows), headers)
    # Use tuple for runtime isinstance and avoid redundant casts for mypy
    if isinstance(rows, str | Path | PathLike):
        return _normalize_from_csv_src(rows, headers)
    seq = cast("Sequence[Any]", rows)
    if seq and isinstance(seq[0], Mapping):
        return _normalize_from_mappings(cast("RowsMapping", seq), headers)
    return _normalize_from_sequences(cast("RowsSequence", seq), headers)


@overload
def table(
    rows: RowsMapping, *, headers: Sequence[str] | None = ..., fmt: TableFormat = ...
) -> str: ...
@overload
def table(
    rows: RowsSequence, *, headers: Sequence[str] | None = ..., fmt: TableFormat = ...
) -> str: ...
@overload
def table(
    rows: DfLike, *, headers: Sequence[str] | None = ..., fmt: TableFormat = ...
) -> str: ...
@overload
def table(
    rows: CsvLike, *, headers: Sequence[str] | None = ..., fmt: TableFormat = ...
) -> str: ...


@render_function("table")
def table(
    rows: RowsLike,
    headers: Sequence[str] | None = None,
    fmt: TableFormat = "csv",
) -> str:
    """Render a small table from mappings, row sequences, a pandas-like DataFrame, or CSV.

    CSV handling:
        ``str`` is interpreted as **CSV text**. To load from a file path, pass a
        ``pathlib.Path`` or ``os.PathLike`` instance.

    Args:
        rows: Data in one of the supported forms (mapping rows, sequence rows,
            DataFrame-like, or CSV text/path object).
        headers: Optional explicit header names. When provided, rows are padded or
            truncated to match the header width.
        fmt: Either ``"pretty"`` (via **PrettyTable**) or ``"csv"`` (via ``csv.writer``).

    Returns:
        A formatted table string.

    Raises:
        RuntimeError: If ``fmt="pretty"`` and PrettyTable is not installed.
        ValueError: If ``fmt`` is not one of the supported values.

    Notes:
        Runtime ``isinstance`` checks use tuples of types for compatibility.
        PrettyTable is lazy-imported.
    """
    hdrs, matrix = _normalize(rows, headers)

    if fmt == "csv":
        buf = StringIO()
        writer = csv.writer(buf)
        if hdrs:
            writer.writerow(hdrs)
        writer.writerows(matrix)
        return buf.getvalue().rstrip()

    if fmt == "pretty":
        try:
            from prettytable import PrettyTable  # lazy import
        except Exception as e:
            raise RuntimeError(
                "fmt='pretty' requires the 'prettytable' package. Install it or use fmt='csv'."
            ) from e
        pt = PrettyTable()
        if hdrs:
            pt.field_names = hdrs
        for row in matrix:
            pt.add_row(row)
        return pt.get_string()

    raise ValueError("fmt must be 'pretty' or 'csv'.")
