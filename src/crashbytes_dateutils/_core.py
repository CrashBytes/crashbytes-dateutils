"""DateTime business helpers — business days, fiscal quarters, relative strings."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

# Monday=0 ... Sunday=6
_SATURDAY = 5
_SUNDAY = 6


def start_of_day(dt: datetime) -> datetime:
    """Return *dt* with time set to 00:00:00."""
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def end_of_day(dt: datetime) -> datetime:
    """Return *dt* with time set to 23:59:59.999999."""
    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)


def start_of_month(d: date) -> date:
    """Return the first day of the month for *d*."""
    return d.replace(day=1)


def end_of_month(d: date) -> date:
    """Return the last day of the month for *d*."""
    if d.month == 12:
        return d.replace(day=31)
    return d.replace(month=d.month + 1, day=1) - timedelta(days=1)


def start_of_year(d: date) -> date:
    """Return January 1 of the year for *d*."""
    return d.replace(month=1, day=1)


def end_of_year(d: date) -> date:
    """Return December 31 of the year for *d*."""
    return d.replace(month=12, day=31)


def is_weekend(d: date) -> bool:
    """Check if *d* is a Saturday or Sunday."""
    return d.weekday() >= _SATURDAY


def is_business_day(d: date, holidays: Sequence[date] = ()) -> bool:
    """Check if *d* is a business day (not weekend, not in *holidays*)."""
    return not is_weekend(d) and d not in holidays


def add_business_days(
    d: date, days: int, holidays: Sequence[date] = ()
) -> date:
    """Add *days* business days to *d*, skipping weekends and *holidays*."""
    if days == 0:
        return d
    step = 1 if days > 0 else -1
    remaining = abs(days)
    current = d
    while remaining > 0:
        current += timedelta(days=step)
        if is_business_day(current, holidays):
            remaining -= 1
    return current


def business_days_between(
    start: date, end: date, holidays: Sequence[date] = ()
) -> int:
    """Count business days between *start* (exclusive) and *end* (inclusive)."""
    if start >= end:
        return 0
    count = 0
    current = start + timedelta(days=1)
    while current <= end:
        if is_business_day(current, holidays):
            count += 1
        current += timedelta(days=1)
    return count


def to_relative_string(d: date, today: date | None = None) -> str:
    """Return a human-readable relative string like "3 days ago" or "in 2 weeks"."""
    if today is None:
        today = date.today()
    delta = (d - today).days
    if delta == 0:
        return "today"
    if delta == 1:
        return "tomorrow"
    if delta == -1:
        return "yesterday"
    abs_days = abs(delta)
    if abs_days < 7:
        unit = "day" if abs_days == 1 else "days"
        label = f"{abs_days} {unit}"
    elif abs_days < 30:
        weeks = abs_days // 7
        unit = "week" if weeks == 1 else "weeks"
        label = f"{weeks} {unit}"
    elif abs_days < 365:
        months = abs_days // 30
        unit = "month" if months == 1 else "months"
        label = f"{months} {unit}"
    else:
        years = abs_days // 365
        unit = "year" if years == 1 else "years"
        label = f"{years} {unit}"
    return f"in {label}" if delta > 0 else f"{label} ago"


def age(birth: date, today: date | None = None) -> int:
    """Calculate age in years from *birth* to *today*."""
    if today is None:
        today = date.today()
    years = today.year - birth.year
    if (today.month, today.day) < (birth.month, birth.day):
        years -= 1
    return years


def fiscal_quarter(d: date, start_month: int = 1) -> int:
    """Return fiscal quarter (1–4) for *d*.

    *start_month* is the first month of the fiscal year (default: January).
    """
    adjusted = (d.month - start_month) % 12
    return adjusted // 3 + 1


def fiscal_year(d: date, start_month: int = 1) -> int:
    """Return fiscal year for *d*.

    *start_month* is the first month of the fiscal year.
    """
    if d.month >= start_month:
        return d.year
    return d.year - 1


def next_business_day(d: date, holidays: Sequence[date] = ()) -> date:
    """Return the next business day after *d*."""
    return add_business_days(d, 1, holidays)


def previous_business_day(d: date, holidays: Sequence[date] = ()) -> date:
    """Return the previous business day before *d*."""
    return add_business_days(d, -1, holidays)
