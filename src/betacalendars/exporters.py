"""Stable JSON, CSV, and Markdown serialization."""

from __future__ import annotations

import csv
import io
import json
from typing import Any

from .models import CalendarRange, MonthGrid
from .week import WEEKDAY_NAMES

MONTH_NAMES = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)


def to_json(value: Any, *, indent: int | None = 2) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        indent=indent,
        separators=None if indent else (",", ":"),
    )


def month_to_csv(grid: MonthGrid) -> str:
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(
        [
            "date",
            "year",
            "month",
            "day",
            "weekday",
            "iso_week",
            "iso_week_year",
            "row",
            "column",
            "in_month",
        ]
    )
    for cell in grid.cells:
        writer.writerow(
            [
                cell.date.isoformat() if cell.date else "",
                cell.year if cell.year is not None else "",
                cell.month if cell.month is not None else "",
                cell.day if cell.day is not None else "",
                cell.weekday,
                cell.iso_week if cell.iso_week is not None else "",
                cell.iso_week_year if cell.iso_week_year is not None else "",
                cell.row,
                cell.column,
                str(cell.in_month).lower(),
            ]
        )
    return output.getvalue()


def _cell_markdown(cell: Any) -> str:
    if cell.day is None:
        return ""
    return str(cell.day) if cell.in_month else f"({cell.day})"


def month_to_markdown(grid: MonthGrid) -> str:
    weekdays = [grid.cells[index].weekday[:3].title() for index in range(7)]
    lines = [
        f"## {MONTH_NAMES[grid.month - 1]} {grid.year}",
        "| " + " | ".join(weekdays) + " |",
        "| " + " | ".join("---" for _ in weekdays) + " |",
    ]
    for row in range(grid.row_count):
        cells = grid.cells[row * 7 : row * 7 + 7]
        lines.append("| " + " | ".join(_cell_markdown(cell) for cell in cells) + " |")
    return "\n".join(lines)


def range_to_csv(value: CalendarRange) -> str:
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(["date", "year", "month", "day", "weekday", "iso_week", "iso_week_year"])
    for item in value.dates:
        iso = item.isocalendar()
        writer.writerow(
            [
                item.isoformat(),
                item.year,
                item.month,
                item.day,
                WEEKDAY_NAMES[item.weekday()].title(),
                iso.week,
                iso.year,
            ]
        )
    return output.getvalue()


def range_to_markdown(value: CalendarRange) -> str:
    lines = ["| Date | Weekday | ISO week | ISO week-year |", "|---|---|---:|---:|"]
    for item in value.dates:
        iso = item.isocalendar()
        weekday = WEEKDAY_NAMES[item.weekday()].title()
        lines.append(f"| {item.isoformat()} | {weekday} | {iso.week} | {iso.year} |")
    return "\n".join(lines)


def year_to_csv(months: tuple[MonthGrid, ...]) -> str:
    """Serialize a year with one CSV header and chronological month sections."""
    parts = [month_to_csv(month).splitlines() for month in months]
    if not parts:
        return ""
    return "\n".join([parts[0][0], *(line for part in parts for line in part[1:])])
