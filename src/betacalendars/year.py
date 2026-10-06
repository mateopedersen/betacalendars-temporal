"""Year-grid generation."""

from __future__ import annotations

from .models import YearGrid
from .month import month_grid


def year_grid(
    year: int,
    *,
    week_start: int | str = "monday",
    fixed_rows: bool = False,
    include_overflow: bool = True,
) -> YearGrid:
    """Build the twelve month grids for ``year`` in chronological order."""
    if not isinstance(year, int) or isinstance(year, bool) or not 1 <= year <= 9999:
        raise ValueError("year must be an integer from 1 through 9999")
    months = tuple(
        month_grid(
            year,
            month,
            week_start=week_start,
            fixed_rows=fixed_rows,
            include_overflow=include_overflow,
        )
        for month in range(1, 13)
    )
    return YearGrid(year, months[0].week_start, fixed_rows, include_overflow, months)
