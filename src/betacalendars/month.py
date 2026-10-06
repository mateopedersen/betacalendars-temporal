"""Month-grid generation."""

from __future__ import annotations

import calendar as _calendar
from datetime import date

from .models import CalendarCell, MonthGrid
from .week import WEEKDAY_NAMES, normalize_weekday


def month_grid(
    year: int,
    month: int,
    *,
    week_start: int | str = "monday",
    fixed_rows: bool = False,
    include_overflow: bool = True,
) -> MonthGrid:
    """Build a month grid with complete weeks and optional adjacent-month cells."""
    if not isinstance(year, int) or isinstance(year, bool) or not 1 <= year <= 9999:
        raise ValueError("year must be an integer from 1 through 9999")
    if not isinstance(month, int) or isinstance(month, bool) or not 1 <= month <= 12:
        raise ValueError("month must be an integer from 1 through 12")
    first_weekday = normalize_weekday(week_start)
    start_name = WEEKDAY_NAMES[first_weekday]
    dates = _calendar.Calendar(firstweekday=first_weekday).monthdatescalendar(year, month)
    if fixed_rows:
        while len(dates) < 6:
            last = dates[-1][-1]
            dates.append([date.fromordinal(last.toordinal() + offset) for offset in range(1, 8)])
    cells: list[CalendarCell] = []
    for row_index, week in enumerate(dates):
        for column_index, actual_date in enumerate(week):
            in_month = actual_date.year == year and actual_date.month == month
            included_date = actual_date if in_month or include_overflow else None
            iso = actual_date.isocalendar()
            cells.append(
                CalendarCell(
                    date=included_date,
                    year=included_date.year if included_date else None,
                    month=included_date.month if included_date else None,
                    day=included_date.day if included_date else None,
                    weekday=WEEKDAY_NAMES[actual_date.weekday()],
                    weekday_index=actual_date.weekday(),
                    row=row_index,
                    column=column_index,
                    iso_week=iso.week if included_date else None,
                    iso_week_year=iso.year if included_date else None,
                    in_month=in_month,
                    is_weekend=actual_date.weekday() >= 5,
                    is_month_start=in_month and actual_date.day == 1,
                    is_month_end=in_month
                    and actual_date.day == _calendar.monthrange(year, month)[1],
                    is_year_start=in_month and actual_date.month == 1 and actual_date.day == 1,
                    is_year_end=in_month and actual_date.month == 12 and actual_date.day == 31,
                )
            )
    return MonthGrid(
        year=year,
        month=month,
        week_start=start_name,
        fixed_rows=fixed_rows,
        include_overflow=include_overflow,
        cells=tuple(cells),
    )
