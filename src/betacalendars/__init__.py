"""Structured, deterministic calendar utilities for Python applications."""

from .boundaries import calendar_boundaries
from .business import (
    business_days_between,
    is_business_day,
    is_weekend,
    next_business_day,
    previous_business_day,
)
from .models import (
    CalendarBoundary,
    CalendarCell,
    CalendarRange,
    MonthGrid,
    RecurrenceRule,
    ValidationDiagnostic,
    ValidationReport,
    YearGrid,
)
from .month import month_grid
from .range import date_range
from .recurrence import annual_date, every_weekday, last_weekday, monthly_date, nth_weekday, weekly
from .validation import validate_month_grid
from .year import year_grid

__version__ = "0.1.0"

__all__ = [
    "CalendarBoundary",
    "CalendarCell",
    "CalendarRange",
    "MonthGrid",
    "RecurrenceRule",
    "ValidationDiagnostic",
    "ValidationReport",
    "YearGrid",
    "annual_date",
    "business_days_between",
    "calendar_boundaries",
    "date_range",
    "every_weekday",
    "is_business_day",
    "is_weekend",
    "last_weekday",
    "month_grid",
    "monthly_date",
    "next_business_day",
    "nth_weekday",
    "previous_business_day",
    "validate_month_grid",
    "weekly",
    "year_grid",
]
