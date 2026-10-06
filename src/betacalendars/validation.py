"""Calendar-grid invariant validation."""

from __future__ import annotations

from calendar import monthrange
from collections import Counter
from datetime import date

from .models import MonthGrid, ValidationDiagnostic, ValidationReport
from .week import WEEKDAY_NAMES


def validate_month_grid(grid: MonthGrid) -> ValidationReport:
    """Check shape, coordinates, chronological dates, and requested-month coverage."""
    diagnostics: list[ValidationDiagnostic] = []
    expected_count = 42 if grid.fixed_rows else None
    if expected_count is not None and len(grid.cells) != expected_count:
        diagnostics.append(
            ValidationDiagnostic(
                "cell_count", f"fixed month grid must contain {expected_count} cells"
            )
        )
    if len(grid.cells) % 7:
        diagnostics.append(ValidationDiagnostic("row_shape", "cell count must be a multiple of 7"))
    if not grid.fixed_rows and not 28 <= len(grid.cells) <= 42:
        diagnostics.append(
            ValidationDiagnostic(
                "compact_shape", "compact grid must contain four to six complete rows"
            )
        )
    dates: list[date] = []
    for index, cell in enumerate(grid.cells):
        expected_row, expected_column = divmod(index, 7)
        if (cell.row, cell.column) != (expected_row, expected_column):
            diagnostics.append(
                ValidationDiagnostic(
                    "coordinate", "row or column does not match cell position", index
                )
            )
        expected_weekday = (WEEKDAY_NAMES.index(grid.week_start) + index) % 7
        if cell.weekday_index != expected_weekday:
            diagnostics.append(
                ValidationDiagnostic(
                    "weekday_sequence", "cell weekday does not match its grid column", index
                )
            )
        if cell.date is not None:
            dates.append(cell.date)
            if cell.date.weekday() != cell.weekday_index:
                diagnostics.append(
                    ValidationDiagnostic(
                        "weekday", "weekday metadata does not match the cell date", index
                    )
                )
            if cell.date.year == grid.year and cell.date.month == grid.month and not cell.in_month:
                diagnostics.append(
                    ValidationDiagnostic(
                        "month_flag", "current-month date is marked as overflow", index
                    )
                )
        elif cell.in_month:
            diagnostics.append(
                ValidationDiagnostic(
                    "missing_month_date", "a current-month cell must have a date", index
                )
            )
    counts = Counter(dates)
    if any(count > 1 for count in counts.values()):
        diagnostics.append(ValidationDiagnostic("duplicate_date", "grid contains duplicate dates"))
    if dates != sorted(dates):
        diagnostics.append(
            ValidationDiagnostic("chronology", "included dates are not chronological")
        )
    month_dates = [
        value for value in dates if value.year == grid.year and value.month == grid.month
    ]
    expected_month_days = [
        date(grid.year, grid.month, day)
        for day in range(1, monthrange(grid.year, grid.month)[1] + 1)
    ]
    if month_dates != expected_month_days:
        diagnostics.append(
            ValidationDiagnostic(
                "month_coverage", "each requested-month date must appear exactly once"
            )
        )
    if grid.fixed_rows and len(grid.cells) == 42 and grid.row_count != 6:
        diagnostics.append(
            ValidationDiagnostic("fixed_rows", "fixed month grid must have six rows")
        )
    return ValidationReport(not diagnostics, tuple(diagnostics))
