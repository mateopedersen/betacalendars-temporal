from datetime import date, datetime

import pytest

from betacalendars import date_range


def test_date_range_is_inclusive_and_consecutive_across_year_end() -> None:
    start, end = date(2026, 12, 20), date(2027, 1, 10)
    value = date_range(start, end)
    assert value.start == start and value.end == end
    assert len(value) == 22
    assert tuple(value)[0] == start and tuple(value)[-1] == end
    assert all(
        (right - left).days == 1 for left, right in zip(value.dates, value.dates[1:], strict=False)
    )


def test_single_day_range_and_invalid_bounds() -> None:
    day = date(2024, 2, 29)
    assert tuple(date_range(day, day)) == (day,)
    with pytest.raises(ValueError):
        date_range(day, date(2024, 2, 28))
    with pytest.raises(TypeError):
        date_range(datetime(2024, 1, 1), datetime(2024, 1, 2))  # type: ignore[arg-type]
