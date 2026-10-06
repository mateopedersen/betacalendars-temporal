from datetime import date

import pytest

from betacalendars import month_grid
from betacalendars.week import WEEKDAY_NAMES


@pytest.mark.parametrize("week_start", WEEKDAY_NAMES)
def test_fixed_grid_has_42_cells_and_valid_coordinates(week_start: str) -> None:
    grid = month_grid(2027, 1, week_start=week_start, fixed_rows=True)
    assert len(grid.cells) == 42
    assert grid.row_count == 6
    assert grid.cells[0].weekday == week_start
    assert grid.validate().valid
    assert {(cell.row, cell.column) for cell in grid.cells} == {
        (row, column) for row in range(6) for column in range(7)
    }


@pytest.mark.parametrize("year", [1900, 1999, 2000, 2004, 2024, 2027, 2028, 2032, 2099, 2100, 2400])
def test_compact_months_cover_each_requested_date_once(year: int) -> None:
    for month in range(1, 13):
        grid = month_grid(year, month)
        assert 28 <= len(grid.cells) <= 42
        current = [cell.date for cell in grid.cells if cell.in_month]
        assert current == [date(year, month, day) for day in range(1, len(current) + 1)]
        assert grid.validate().valid


def test_gregorian_leap_century_rules() -> None:
    assert len([c for c in month_grid(1900, 2).cells if c.in_month]) == 28
    assert len([c for c in month_grid(2000, 2).cells if c.in_month]) == 29
    assert len([c for c in month_grid(2100, 2).cells if c.in_month]) == 28
    assert len([c for c in month_grid(2400, 2).cells if c.in_month]) == 29


def test_included_overflow_dates_are_consecutive() -> None:
    grid = month_grid(2027, 1)
    values = [cell.date for cell in grid.cells]
    assert all(value is not None for value in values)
    assert all((right - left).days == 1 for left, right in zip(values, values[1:], strict=False))


def test_excluded_overflow_keeps_coordinates_without_fake_dates() -> None:
    grid = month_grid(2027, 1, include_overflow=False)
    assert len(grid.cells) % 7 == 0
    overflow = [cell for cell in grid.cells if not cell.in_month]
    assert overflow
    assert all(cell.date is None and cell.day is None for cell in overflow)
    assert grid.validate().valid


def test_invalid_month_inputs_are_rejected() -> None:
    with pytest.raises(ValueError):
        month_grid(2027, 13)
    with pytest.raises(ValueError):
        month_grid(2027, 1, week_start="funday")
