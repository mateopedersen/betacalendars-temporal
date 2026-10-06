import csv
import json
from io import StringIO

from betacalendars import date_range, month_grid


def test_month_json_is_deterministic_and_iso_formatted() -> None:
    grid = month_grid(2027, 1)
    assert grid.to_json() == grid.to_json()
    value = json.loads(grid.to_json())
    assert value["cells"][0]["date"] == grid.cells[0].date.isoformat()


def test_csv_quotes_and_uses_one_row_per_cell() -> None:
    text = month_grid(2027, 1, fixed_rows=True).to_csv()
    rows = list(csv.reader(StringIO(text)))
    assert rows[0] == [
        "date",
        "year",
        "month",
        "day",
        "weekday",
        "iso_week",
        "iso_week_year",
        "row",
        "column",
        "in_month",
    ]
    assert len(rows) == 43


def test_markdown_and_range_exports_are_useful() -> None:
    grid = month_grid(2027, 1)
    assert "| Mon | Tue | Wed | Thu | Fri | Sat | Sun |" in grid.to_markdown()
    assert "## January 2027" in grid.to_markdown()
    period = date_range(
        __import__("datetime").date(2026, 12, 31), __import__("datetime").date(2027, 1, 1)
    )
    assert "2026-12-31" in period.to_json()
    assert "2027-01-01" in period.to_csv()
