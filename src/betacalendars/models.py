"""Immutable calendar data models."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass(frozen=True, slots=True)
class CalendarCell:
    """One calendar-grid coordinate; excluded overflow cells have no date or day."""

    date: date | None
    year: int | None
    month: int | None
    day: int | None
    weekday: str
    weekday_index: int
    row: int
    column: int
    iso_week: int | None
    iso_week_year: int | None
    in_month: bool
    is_weekend: bool
    is_month_start: bool
    is_month_end: bool
    is_year_start: bool
    is_year_end: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "date": self.date.isoformat() if self.date else None,
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "weekday": self.weekday,
            "weekday_index": self.weekday_index,
            "row": self.row,
            "column": self.column,
            "iso_week": self.iso_week,
            "iso_week_year": self.iso_week_year,
            "in_month": self.in_month,
            "is_weekend": self.is_weekend,
            "is_month_start": self.is_month_start,
            "is_month_end": self.is_month_end,
            "is_year_start": self.is_year_start,
            "is_year_end": self.is_year_end,
        }


@dataclass(frozen=True, slots=True)
class MonthGrid:
    """Calendar cells for one month, arranged in complete Monday-to-Sunday rows."""

    year: int
    month: int
    week_start: str
    fixed_rows: bool
    include_overflow: bool
    cells: tuple[CalendarCell, ...]

    @property
    def row_count(self) -> int:
        return len(self.cells) // 7

    def validate(self) -> ValidationReport:
        from .validation import validate_month_grid

        return validate_month_grid(self)

    def to_dict(self) -> dict[str, Any]:
        return {
            "year": self.year,
            "month": self.month,
            "week_start": self.week_start,
            "fixed_rows": self.fixed_rows,
            "include_overflow": self.include_overflow,
            "row_count": self.row_count,
            "cells": [cell.to_dict() for cell in self.cells],
        }

    def to_json(self, *, indent: int | None = 2) -> str:
        from .exporters import to_json

        return to_json(self.to_dict(), indent=indent)

    def to_csv(self) -> str:
        from .exporters import month_to_csv

        return month_to_csv(self)

    def to_markdown(self) -> str:
        from .exporters import month_to_markdown

        return month_to_markdown(self)


@dataclass(frozen=True, slots=True)
class YearGrid:
    """The twelve month grids for a calendar year."""

    year: int
    week_start: str
    fixed_rows: bool
    include_overflow: bool
    months: tuple[MonthGrid, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "year": self.year,
            "week_start": self.week_start,
            "fixed_rows": self.fixed_rows,
            "include_overflow": self.include_overflow,
            "months": [month.to_dict() for month in self.months],
        }

    def to_json(self, *, indent: int | None = 2) -> str:
        from .exporters import to_json

        return to_json(self.to_dict(), indent=indent)

    def to_markdown(self) -> str:
        return "\n\n".join(month.to_markdown() for month in self.months)


@dataclass(frozen=True, slots=True)
class CalendarRange:
    """An inclusive, consecutive date range."""

    start: date
    end: date
    dates: tuple[date, ...]

    def __iter__(self) -> Iterator[date]:
        return iter(self.dates)

    def __len__(self) -> int:
        return len(self.dates)

    def to_dict(self) -> dict[str, Any]:
        return {
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "dates": [item.isoformat() for item in self.dates],
        }

    def to_json(self, *, indent: int | None = 2) -> str:
        from .exporters import to_json

        return to_json(self.to_dict(), indent=indent)

    def to_csv(self) -> str:
        from .exporters import range_to_csv

        return range_to_csv(self)

    def to_markdown(self) -> str:
        from .exporters import range_to_markdown

        return range_to_markdown(self)


@dataclass(frozen=True, slots=True)
class CalendarBoundary:
    """Useful year and ISO-week-year boundary facts."""

    year: int
    year_start: date
    year_end: date
    month_starts: tuple[date, ...]
    month_ends: tuple[date, ...]
    is_leap_year: bool
    february_days: int
    iso_week_year_transition_dates: tuple[date, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "year": self.year,
            "year_start": self.year_start.isoformat(),
            "year_end": self.year_end.isoformat(),
            "month_starts": [value.isoformat() for value in self.month_starts],
            "month_ends": [value.isoformat() for value in self.month_ends],
            "is_leap_year": self.is_leap_year,
            "february_days": self.february_days,
            "iso_week_year_transition_dates": [
                value.isoformat() for value in self.iso_week_year_transition_dates
            ],
        }

    def to_json(self, *, indent: int | None = 2) -> str:
        from .exporters import to_json

        return to_json(self.to_dict(), indent=indent)


@dataclass(frozen=True, slots=True)
class ValidationDiagnostic:
    """One detected calendar-grid invariant violation."""

    code: str
    message: str
    cell_index: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {"code": self.code, "message": self.message, "cell_index": self.cell_index}


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Structured result for month-grid validation."""

    valid: bool
    diagnostics: tuple[ValidationDiagnostic, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "diagnostics": [item.to_dict() for item in self.diagnostics],
        }


@dataclass(frozen=True, slots=True)
class RecurrenceRule:
    """A bounded recurrence specification. See :meth:`expand` for supported rules."""

    frequency: str
    interval: int = 1
    weekdays: tuple[int, ...] = ()
    day_of_month: int | None = None
    month: int | None = None
    weekday: int | None = None
    ordinal: int | None = None
    invalid_day: str = "skip"

    @classmethod
    def every_weekday(cls, weekdays: tuple[int | str, ...] = (0, 1, 2, 3, 4)) -> RecurrenceRule:
        from .week import normalize_weekday

        values = tuple(sorted({normalize_weekday(value) for value in weekdays}))
        if not values:
            raise ValueError("at least one weekday is required")
        return cls("weekdays", weekdays=values)

    @classmethod
    def weekly(cls, weekdays: tuple[int | str, ...], *, interval: int = 1) -> RecurrenceRule:
        from .week import normalize_weekday

        values = tuple(sorted({normalize_weekday(value) for value in weekdays}))
        if not values:
            raise ValueError("at least one weekday is required")
        if interval < 1:
            raise ValueError("interval must be at least 1")
        return cls("weekly", interval=interval, weekdays=values)

    @classmethod
    def monthly_date(cls, day: int, *, invalid_day: str = "skip") -> RecurrenceRule:
        if not 1 <= day <= 31:
            raise ValueError("day must be between 1 and 31")
        if invalid_day not in {"skip", "last_day"}:
            raise ValueError("invalid_day must be 'skip' or 'last_day'")
        return cls("monthly_date", day_of_month=day, invalid_day=invalid_day)

    @classmethod
    def nth_weekday(cls, *, weekday: int | str, ordinal: int) -> RecurrenceRule:
        from .week import normalize_weekday

        if ordinal not in {-1, 1, 2, 3, 4, 5}:
            raise ValueError("ordinal must be 1 through 5 or -1 for the last weekday")
        return cls("nth_weekday", weekday=normalize_weekday(weekday), ordinal=ordinal)

    @classmethod
    def last_weekday(cls, weekday: int | str) -> RecurrenceRule:
        return cls.nth_weekday(weekday=weekday, ordinal=-1)

    @classmethod
    def annual_date(cls, month: int, day: int, *, invalid_day: str = "skip") -> RecurrenceRule:
        from .recurrence import normalize_month_day_policy

        if not 1 <= month <= 12 or not 1 <= day <= 31:
            raise ValueError("month and day must be valid calendar values")
        policy = normalize_month_day_policy(invalid_day)
        if month == 2 and day == 29 and policy not in {"skip", "feb28", "mar1", "last_day"}:
            raise ValueError("February 29 policy must be 'skip', 'feb28', 'mar1', or 'last_day'")
        return cls("annual_date", month=month, day_of_month=day, invalid_day=policy)

    def expand(self, start: date, end: date) -> tuple[date, ...]:
        from .recurrence import expand_rule

        return expand_rule(self, start, end)
