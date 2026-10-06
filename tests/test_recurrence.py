from datetime import date

import pytest

from betacalendars import RecurrenceRule, annual_date, every_weekday, last_weekday, weekly


def test_every_weekday_is_bounded_and_inclusive() -> None:
    days = every_weekday(date(2027, 1, 1), date(2027, 1, 8))
    assert days == (
        date(2027, 1, 1),
        date(2027, 1, 4),
        date(2027, 1, 5),
        date(2027, 1, 6),
        date(2027, 1, 7),
        date(2027, 1, 8),
    )


def test_weekly_interval_and_selected_weekdays() -> None:
    days = weekly(date(2027, 1, 1), date(2027, 1, 31), weekdays=("monday",), interval=2)
    assert days == (date(2027, 1, 4), date(2027, 1, 18))


def test_monthly_date_skip_or_clamp() -> None:
    skip = RecurrenceRule.monthly_date(31).expand(date(2027, 4, 1), date(2027, 6, 30))
    clamp = RecurrenceRule.monthly_date(31, invalid_day="last_day").expand(
        date(2027, 4, 1), date(2027, 6, 30)
    )
    assert skip == (date(2027, 5, 31),)
    assert clamp == (date(2027, 4, 30), date(2027, 5, 31), date(2027, 6, 30))


def test_nth_and_last_weekdays() -> None:
    first_mondays = RecurrenceRule.nth_weekday(weekday="monday", ordinal=1).expand(
        date(2027, 1, 1), date(2027, 3, 31)
    )
    last_fridays = last_weekday(date(2027, 1, 1), date(2027, 3, 31), "friday")
    assert first_mondays == (date(2027, 1, 4), date(2027, 2, 1), date(2027, 3, 1))
    assert last_fridays == (date(2027, 1, 29), date(2027, 2, 26), date(2027, 3, 26))


def test_annual_february_29_policies_and_invalid_bounds() -> None:
    start, end = date(2023, 1, 1), date(2028, 12, 31)
    assert annual_date(start, end, 2, 29) == (date(2024, 2, 29), date(2028, 2, 29))
    assert annual_date(start, end, 2, 29, invalid_day="feb28") == (
        date(2023, 2, 28),
        date(2024, 2, 29),
        date(2025, 2, 28),
        date(2026, 2, 28),
        date(2027, 2, 28),
        date(2028, 2, 29),
    )
    with pytest.raises(ValueError):
        RecurrenceRule.every_weekday().expand(end, start)
