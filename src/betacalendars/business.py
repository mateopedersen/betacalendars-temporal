"""Business-day helpers with caller-provided weekend and exclusion policy."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import date, timedelta

from .week import normalize_weekday


def _weekend_set(weekend: Iterable[int | str]) -> frozenset[int]:
    result = frozenset(normalize_weekday(day) for day in weekend)
    if len(result) == 7:
        raise ValueError("weekend cannot contain all seven weekdays")
    return result


def is_weekend(value: date, *, weekend: Iterable[int | str] = (5, 6)) -> bool:
    """Return whether ``value`` falls on a caller-selected weekend day."""
    return value.weekday() in _weekend_set(weekend)


def is_business_day(
    value: date,
    *,
    weekend: Iterable[int | str] = (5, 6),
    excluded_dates: Iterable[date] | None = None,
) -> bool:
    """Return whether a date is not a weekend or an explicitly excluded day."""
    return not is_weekend(value, weekend=weekend) and value not in frozenset(excluded_dates or ())


def business_days_between(
    start: date,
    end: date,
    *,
    weekend: Iterable[int | str] = (5, 6),
    excluded_dates: Iterable[date] | None = None,
) -> tuple[date, ...]:
    """Return business dates from ``start`` through ``end``, inclusive."""
    if start > end:
        raise ValueError("start must be on or before end")
    excluded = frozenset(excluded_dates or ())
    days = (end - start).days
    return tuple(
        day
        for offset in range(days + 1)
        if is_business_day(
            day := start + timedelta(days=offset), weekend=weekend, excluded_dates=excluded
        )
    )


def next_business_day(
    value: date,
    *,
    weekend: Iterable[int | str] = (5, 6),
    excluded_dates: Iterable[date] | None = None,
    include_start: bool = True,
) -> date:
    """Return the first business day on or after ``value`` (or after it)."""
    candidate = value if include_start else value + timedelta(days=1)
    while not is_business_day(candidate, weekend=weekend, excluded_dates=excluded_dates):
        candidate += timedelta(days=1)
    return candidate


def previous_business_day(
    value: date,
    *,
    weekend: Iterable[int | str] = (5, 6),
    excluded_dates: Iterable[date] | None = None,
    include_start: bool = True,
) -> date:
    """Return the first business day on or before ``value`` (or before it)."""
    candidate = value if include_start else value - timedelta(days=1)
    while not is_business_day(candidate, weekend=weekend, excluded_dates=excluded_dates):
        candidate -= timedelta(days=1)
    return candidate
