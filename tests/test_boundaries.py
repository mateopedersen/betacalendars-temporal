from datetime import date

import pytest

from betacalendars import calendar_boundaries


@pytest.mark.parametrize(
    ("year", "leap", "feb_days"),
    [(1900, False, 28), (2000, True, 29), (2100, False, 28), (2400, True, 29)],
)
def test_leap_century_boundary_rules(year: int, leap: bool, feb_days: int) -> None:
    value = calendar_boundaries(year)
    assert value.is_leap_year is leap
    assert value.february_days == feb_days
    assert value.year_start == date(year, 1, 1)
    assert value.year_end == date(year, 12, 31)
    assert len(value.month_starts) == len(value.month_ends) == 12


def test_iso_week_year_transition_metadata() -> None:
    value = calendar_boundaries(2021)
    assert date(2021, 1, 1) in value.iso_week_year_transition_dates
    assert date(2021, 1, 3) in value.iso_week_year_transition_dates
    assert date(2021, 1, 4) not in value.iso_week_year_transition_dates
