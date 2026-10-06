"""Weekday parsing and calendar week-start helpers."""

from __future__ import annotations

from typing import Final

WEEKDAY_NAMES: Final[tuple[str, ...]] = (
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
)


def normalize_weekday(value: int | str) -> int:
    """Return Monday=0 through Sunday=6 for a name or integer."""
    if isinstance(value, bool):
        raise ValueError("weekday must be a name or an integer from 0 through 6")
    if isinstance(value, int):
        if 0 <= value <= 6:
            return value
        raise ValueError("weekday integer must be from 0 through 6")
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in WEEKDAY_NAMES:
            return WEEKDAY_NAMES.index(normalized)
    raise ValueError(f"unknown weekday: {value!r}")


def weekday_name(value: int | str) -> str:
    """Return the canonical lowercase weekday name."""
    return WEEKDAY_NAMES[normalize_weekday(value)]
