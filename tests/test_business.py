from datetime import date

from betacalendars import (
    business_days_between,
    is_business_day,
    is_weekend,
    next_business_day,
    previous_business_day,
)


def test_weekend_and_caller_excluded_dates() -> None:
    holiday = date(2027, 1, 4)
    assert is_weekend(date(2027, 1, 2))
    assert not is_weekend(date(2027, 1, 3), weekend=("friday", "saturday"))
    assert not is_business_day(holiday, excluded_dates={holiday})
    assert business_days_between(date(2027, 1, 1), date(2027, 1, 5), excluded_dates={holiday}) == (
        date(2027, 1, 1),
        date(2027, 1, 5),
    )


def test_next_and_previous_business_day() -> None:
    saturday = date(2027, 1, 2)
    assert next_business_day(saturday) == date(2027, 1, 4)
    assert previous_business_day(saturday) == date(2027, 1, 1)
