# API notes

The public API is exported from `betacalendars`. `month_grid` and `year_grid` accept all seven weekday names or Python weekday indexes (Monday is 0). Grid cells always form full weeks. Fixed grids contain six rows; compact grids contain four to six rows. `include_overflow=False` keeps out-of-month coordinates but sets their date-related values to `None`.

`date_range` is inclusive at both ends and rejects reverse or unbounded inputs. Recurrence rules expand only when explicit start and end dates are provided. Weekly intervals are counted from the Monday-start week containing the lower bound. Monthly dates beyond a month's end are skipped by default or clamped when `invalid_day="last_day"` is selected. Annual February 29 rules can skip non-leap years or use February 28 / March 1.

Business-day functions have no holiday assumptions. Pass excluded dates from the caller's own jurisdictional source.

All serializers are local and deterministic. JSON dates use ISO 8601 strings; CSV output uses the standard CSV writer; Markdown uses plain tables.
