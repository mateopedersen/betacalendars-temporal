"""Inclusive date-range helpers."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from .models import CalendarRange


def date_range(start: date, end: date) -> CalendarRange:
    """Return an inclusive range of consecutive dates."""
    if not isinstance(start, date) or isinstance(start, datetime):
        raise TypeError("start must be a datetime.date")
    if not isinstance(end, date) or isinstance(end, datetime):
        raise TypeError("end must be a datetime.date")
    if start > end:
        raise ValueError("start must be on or before end")
    count = (end - start).days + 1
    values = tuple(start + timedelta(days=offset) for offset in range(count))
    return CalendarRange(start, end, values)
