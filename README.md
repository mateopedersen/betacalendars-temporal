# Beta Calendars Temporal Toolkit

Deterministic calendar grids, date ranges, recurrence helpers, and calendar boundary utilities for Python applications. It builds on Python's `datetime` and `calendar` modules and returns immutable, presentation-neutral data suitable for applications, reports, fixtures, and command-line use.

## Why this exists

Application code often needs more than a month matrix: it needs explicit overflow cells, stable ISO-week metadata, date ranges, bounded recurrence expansion, validation diagnostics, and predictable export formats. This package provides those structures without replacing Python's date types or making network calls.

## Installation

### Pixi

```sh
pixi workspace channel add --prepend https://prefix.dev/conda-forge https://prefix.dev/mateopedersen/betacalendars
pixi add betacalendars-temporal
```

### Conda or Mamba

```sh
conda install --override-channels -c https://prefix.dev/mateopedersen/betacalendars -c conda-forge betacalendars-temporal
```

### Python source checkout

```sh
git clone https://github.com/mateopedersen/betacalendars-temporal.git
cd betacalendars-temporal
python -m pip install .
```

Python 3.11 or later is supported. Runtime dependencies: none.

## Quick start

```python
from betacalendars import month_grid

grid = month_grid(2027, 1, week_start="monday", fixed_rows=True)
assert len(grid.cells) == 42
print(grid.to_markdown())
```

## Month grids

`month_grid(year, month, ...)` returns an immutable `MonthGrid`. Each `CalendarCell` carries its date, position, weekday, ISO week and year, in-month status, weekend status, and month/year boundary flags when a date is included.

```python
from betacalendars import month_grid

grid = month_grid(2027, 1, week_start="sunday", fixed_rows=False)
report = grid.validate()
assert report.valid
```

All seven weekday names are accepted for `week_start`. The default is Monday.

## Year grids

`year_grid(2027, week_start="monday")` returns twelve `MonthGrid` instances in January–December order. The default uses compact layouts; `fixed_rows=True` makes each month a six-by-seven grid.

## Week starts and overflow dates

Set `week_start` to `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`, or `sunday`. With `include_overflow=True` (the default), adjacent-month cells have their actual dates. With `include_overflow=False`, those cells remain in the grid as coordinate-only cells: their date and day values are `None`, so the model does not imply a date that is not part of the requested month.

## Date ranges

Ranges are inclusive and bounded by the caller:

```python
from datetime import date
from betacalendars import date_range

period = date_range(date(2026, 12, 20), date(2027, 1, 10))
assert len(period) == 22
```

`CalendarRange` is iterable over consecutive `date` values and can produce JSON, CSV, or Markdown.

## Recurrence rules

Recurrence expansion always takes a start and end date. Helpers cover selected weekdays, weekly schedules, monthly dates, nth or last weekdays, and annual dates.

```python
from datetime import date
from betacalendars import RecurrenceRule

first_mondays = RecurrenceRule.nth_weekday(weekday="monday", ordinal=1)
dates = first_mondays.expand(date(2027, 1, 1), date(2027, 12, 31))
```

A monthly date that does not exist in a month is skipped by default; callers can choose the last day of that month. Annual February 29 recurrences also have an explicit policy.

## Business-day helpers

`is_weekend`, `is_business_day`, `business_days_between`, `next_business_day`, and `previous_business_day` use caller-supplied weekend days and excluded dates. No built-in national holiday database is bundled.

## Boundary analysis

`calendar_boundaries(year)` reports the first and last day of the year, every month start and end, leap-year status, February length, and dates whose ISO week-year differs from the calendar year. This is useful when testing year-end behavior.

## JSON

`MonthGrid.to_json()` and the equivalent year/range exporters use ISO 8601 dates, sorted object keys, and no generated timestamps or machine-specific values.

## CSV

`MonthGrid.to_csv()` writes one row per cell with stable columns for date, year, month, day, weekday, ISO week, row, column, and in-month status. Coordinate-only overflow cells have empty date fields.

## Markdown

`to_markdown()` renders a readable weekday table. Included overflow days appear in parentheses; omitted overflow days leave the cell blank.

## CLI

```sh
betacal --version
betacal month 2027 1
betacal month 2027 1 --week-start monday --format json
betacal month 2027 1 --format csv
betacal year 2027 --format json
betacal range 2026-12-20 2027-01-10
betacal boundaries 2027
```

The command works offline. It prints no promotional content.

## Testing calendar applications

The project tests Gregorian leap-century rules, every weekday as the first day of a month, fixed and compact layouts, year transitions, ISO week-years, recurrence boundaries, business-day behavior, serializers, validation diagnostics, and CLI exit behavior.

## API stability

Version 0.x is an initial public API. Data models are frozen; field and function changes may occur before 1.0 and will be recorded in the changelog.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Report security issues privately as described in [SECURITY.md](SECURITY.md).

## License

MIT. See [LICENSE](LICENSE).

## Project

Maintained by [Beta Calendars](https://www.betacalendars.com/). Source, documentation, and issue tracking are on [GitHub](https://github.com/mateopedersen/betacalendars-temporal).
