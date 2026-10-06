"""Offline command-line interface for calendar generation."""

from __future__ import annotations

import argparse
import sys
from datetime import date

from . import __version__
from .boundaries import calendar_boundaries
from .exporters import year_to_csv
from .month import month_grid
from .range import date_range
from .year import year_grid

_FORMATS = ("text", "json", "csv", "markdown")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="betacal", description="Generate deterministic calendar data."
    )
    parser.add_argument("--version", action="version", version=f"betacal {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    month = commands.add_parser("month", help="render one month")
    month.add_argument("year", type=int)
    month.add_argument("month", type=int)
    month.add_argument(
        "--week-start",
        default="monday",
        choices=("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"),
    )
    month.add_argument("--fixed-rows", action="store_true", help="always render six rows")
    month.add_argument(
        "--no-overflow", action="store_true", help="leave adjacent-month cells date-free"
    )
    month.add_argument("--format", choices=_FORMATS, default="markdown")

    year = commands.add_parser("year", help="render all twelve months")
    year.add_argument("year", type=int)
    year.add_argument(
        "--week-start",
        default="monday",
        choices=("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"),
    )
    year.add_argument("--fixed-rows", action="store_true")
    year.add_argument("--no-overflow", action="store_true")
    year.add_argument("--format", choices=_FORMATS, default="json")

    period = commands.add_parser("range", help="list inclusive dates between two ISO dates")
    period.add_argument("start", type=date.fromisoformat)
    period.add_argument("end", type=date.fromisoformat)
    period.add_argument("--format", choices=_FORMATS, default="csv")

    boundaries = commands.add_parser("boundaries", help="show year and ISO-week boundary details")
    boundaries.add_argument("year", type=int)
    boundaries.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def _render(args: argparse.Namespace) -> str:
    if args.command == "month":
        month = month_grid(
            args.year,
            args.month,
            week_start=args.week_start,
            fixed_rows=args.fixed_rows,
            include_overflow=not args.no_overflow,
        )
        if args.format == "json":
            return month.to_json()
        if args.format == "csv":
            return month.to_csv()
        return month.to_markdown()
    if args.command == "year":
        year = year_grid(
            args.year,
            week_start=args.week_start,
            fixed_rows=args.fixed_rows,
            include_overflow=not args.no_overflow,
        )
        if args.format == "json":
            return year.to_json()
        if args.format == "csv":
            return year_to_csv(year.months)
        return year.to_markdown()
    if args.command == "range":
        value = date_range(args.start, args.end)
        if args.format == "json":
            return value.to_json()
        if args.format == "csv":
            return value.to_csv()
        return value.to_markdown()
    result = calendar_boundaries(args.year)
    if args.format == "json":
        return result.to_json()
    transitions = ", ".join(map(str, result.iso_week_year_transition_dates)) or "none"
    return (
        f"Year: {result.year}\nStart: {result.year_start}\nEnd: {result.year_end}\n"
        f"Leap year: {result.is_leap_year}\nFebruary days: {result.february_days}\n"
        f"ISO week-year transitions: {transitions}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        output = _render(args)
    except (TypeError, ValueError) as error:
        print(f"betacal: {error}", file=sys.stderr)
        return 2
    print(output)
    return 0
