"""Year and ISO week-year boundary analysis."""

from __future__ import annotations

import calendar
from datetime import date

from .models import CalendarBoundary


def calendar_boundaries(year: int) -> CalendarBoundary:
    """Return year/month edges, leap-year information, and ISO year transitions."""
    if not isinstance(year, int) or isinstance(year, bool) or not 1 <= year <= 9999:
        raise ValueError("year must be an integer from 1 through 9999")
    starts = tuple(date(year, month, 1) for month in range(1, 13))
    ends = tuple(date(year, month, calendar.monthrange(year, month)[1]) for month in range(1, 13))
    transitions: set[date] = set()
    for day in range(1, 8):
        candidate = date(year, 1, day)
        if candidate.isocalendar().year != year:
            transitions.add(candidate)
    for day in range(25, 32):
        candidate = date(year, 12, day)
        if candidate.isocalendar().year != year:
            transitions.add(candidate)
    february_days = calendar.monthrange(year, 2)[1]
    return CalendarBoundary(
        year,
        date(year, 1, 1),
        date(year, 12, 31),
        starts,
        ends,
        calendar.isleap(year),
        february_days,
        tuple(sorted(transitions)),
    )
