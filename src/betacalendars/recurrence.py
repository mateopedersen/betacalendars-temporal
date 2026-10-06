"""Bounded recurrence expansion utilities."""

from __future__ import annotations

import calendar
from collections.abc import Iterator
from datetime import date, datetime, timedelta

from .models import RecurrenceRule


def normalize_month_day_policy(value: str) -> str:
    policy = value.strip().lower()
    if policy not in {"skip", "last_day", "feb28", "mar1"}:
        raise ValueError("policy must be 'skip', 'last_day', 'feb28', or 'mar1'")
    return policy


def _validate_bounds(start: date, end: date) -> None:
    if (
        not isinstance(start, date)
        or isinstance(start, datetime)
        or not isinstance(end, date)
        or isinstance(end, datetime)
    ):
        raise TypeError("start and end must be datetime.date values")
    if start > end:
        raise ValueError("start must be on or before end")


def _months(start: date, end: date) -> Iterator[tuple[int, int]]:
    year, month = start.year, start.month
    while (year, month) <= (end.year, end.month):
        yield year, month
        if month == 12:
            year, month = year + 1, 1
        else:
            month += 1


def _monthly_date(year: int, month: int, day: int, invalid_day: str) -> date | None:
    max_day = calendar.monthrange(year, month)[1]
    if day <= max_day:
        return date(year, month, day)
    if invalid_day == "last_day":
        return date(year, month, max_day)
    return None


def _nth_weekday(year: int, month: int, weekday: int, ordinal: int) -> date | None:
    last_day = calendar.monthrange(year, month)[1]
    if ordinal == -1:
        candidate = date(year, month, last_day)
        return candidate - timedelta(days=(candidate.weekday() - weekday) % 7)
    first = date(year, month, 1)
    day = 1 + (weekday - first.weekday()) % 7 + 7 * (ordinal - 1)
    return date(year, month, day) if day <= last_day else None


def expand_rule(rule: RecurrenceRule, start: date, end: date) -> tuple[date, ...]:
    """Expand a recurrence rule over inclusive finite bounds."""
    _validate_bounds(start, end)
    values: list[date] = []
    if rule.frequency in {"weekdays", "weekly"}:
        first_monday = start + timedelta(days=(-start.weekday()) % 7)
        for offset in range((end - start).days + 1):
            current = start + timedelta(days=offset)
            week_index = max(0, (current - first_monday).days // 7)
            if current.weekday() in rule.weekdays and (
                rule.frequency == "weekdays" or week_index % rule.interval == 0
            ):
                values.append(current)
        return tuple(values)
    if rule.frequency == "monthly_date":
        assert rule.day_of_month is not None
        for year, month in _months(start, end):
            monthly_value = _monthly_date(year, month, rule.day_of_month, rule.invalid_day)
            if monthly_value is not None and start <= monthly_value <= end:
                values.append(monthly_value)
        return tuple(values)
    if rule.frequency == "nth_weekday":
        assert rule.weekday is not None and rule.ordinal is not None
        for year, month in _months(start, end):
            weekday_value = _nth_weekday(year, month, rule.weekday, rule.ordinal)
            if weekday_value is not None and start <= weekday_value <= end:
                values.append(weekday_value)
        return tuple(values)
    if rule.frequency == "annual_date":
        assert rule.month is not None and rule.day_of_month is not None
        for year in range(start.year, end.year + 1):
            max_day = calendar.monthrange(year, rule.month)[1]
            if rule.day_of_month <= max_day:
                current = date(year, rule.month, rule.day_of_month)
            elif rule.month == 2 and rule.day_of_month == 29:
                if rule.invalid_day in {"feb28", "last_day"}:
                    current = date(year, 2, 28)
                elif rule.invalid_day == "mar1":
                    current = date(year, 3, 1)
                else:
                    continue
            elif rule.invalid_day == "last_day":
                current = date(year, rule.month, max_day)
            else:
                continue
            if start <= current <= end:
                values.append(current)
        return tuple(values)
    raise ValueError(f"unsupported recurrence frequency: {rule.frequency!r}")


def every_weekday(
    start: date, end: date, *, weekdays: tuple[int | str, ...] = (0, 1, 2, 3, 4)
) -> tuple[date, ...]:
    return RecurrenceRule.every_weekday(weekdays).expand(start, end)


def weekly(
    start: date, end: date, *, weekdays: tuple[int | str, ...], interval: int = 1
) -> tuple[date, ...]:
    return RecurrenceRule.weekly(weekdays, interval=interval).expand(start, end)


def monthly_date(
    start: date, end: date, day: int, *, invalid_day: str = "skip"
) -> tuple[date, ...]:
    return RecurrenceRule.monthly_date(day, invalid_day=invalid_day).expand(start, end)


def nth_weekday(start: date, end: date, *, weekday: int | str, ordinal: int) -> tuple[date, ...]:
    return RecurrenceRule.nth_weekday(weekday=weekday, ordinal=ordinal).expand(start, end)


def last_weekday(start: date, end: date, weekday: int | str) -> tuple[date, ...]:
    return RecurrenceRule.last_weekday(weekday).expand(start, end)


def annual_date(
    start: date, end: date, month: int, day: int, *, invalid_day: str = "skip"
) -> tuple[date, ...]:
    return RecurrenceRule.annual_date(month, day, invalid_day=invalid_day).expand(start, end)
