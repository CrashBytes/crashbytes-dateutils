"""Tests for crashbytes-dateutils."""

from __future__ import annotations

from datetime import date, datetime

from crashbytes_dateutils import (
    add_business_days,
    age,
    business_days_between,
    end_of_day,
    end_of_month,
    end_of_year,
    fiscal_quarter,
    fiscal_year,
    is_business_day,
    is_weekend,
    next_business_day,
    previous_business_day,
    start_of_day,
    start_of_month,
    start_of_year,
    to_relative_string,
)


class TestStartEndOfDay:
    def test_start_of_day(self) -> None:
        dt = datetime(2024, 6, 15, 14, 30, 45, 123456)
        result = start_of_day(dt)
        assert result == datetime(2024, 6, 15, 0, 0, 0, 0)

    def test_end_of_day(self) -> None:
        dt = datetime(2024, 6, 15, 14, 30, 45)
        result = end_of_day(dt)
        assert result == datetime(2024, 6, 15, 23, 59, 59, 999999)


class TestStartEndOfMonth:
    def test_start_of_month(self) -> None:
        assert start_of_month(date(2024, 6, 15)) == date(2024, 6, 1)

    def test_end_of_month_june(self) -> None:
        assert end_of_month(date(2024, 6, 15)) == date(2024, 6, 30)

    def test_end_of_month_february_leap(self) -> None:
        assert end_of_month(date(2024, 2, 1)) == date(2024, 2, 29)

    def test_end_of_month_february_non_leap(self) -> None:
        assert end_of_month(date(2023, 2, 1)) == date(2023, 2, 28)

    def test_end_of_month_december(self) -> None:
        assert end_of_month(date(2024, 12, 1)) == date(2024, 12, 31)


class TestStartEndOfYear:
    def test_start_of_year(self) -> None:
        assert start_of_year(date(2024, 6, 15)) == date(2024, 1, 1)

    def test_end_of_year(self) -> None:
        assert end_of_year(date(2024, 6, 15)) == date(2024, 12, 31)


class TestWeekend:
    def test_saturday(self) -> None:
        assert is_weekend(date(2024, 6, 15)) is True  # Saturday

    def test_sunday(self) -> None:
        assert is_weekend(date(2024, 6, 16)) is True  # Sunday

    def test_monday(self) -> None:
        assert is_weekend(date(2024, 6, 17)) is False  # Monday

    def test_friday(self) -> None:
        assert is_weekend(date(2024, 6, 14)) is False  # Friday


class TestBusinessDay:
    def test_weekday(self) -> None:
        assert is_business_day(date(2024, 6, 17)) is True  # Monday

    def test_weekend(self) -> None:
        assert is_business_day(date(2024, 6, 15)) is False  # Saturday

    def test_holiday(self) -> None:
        holidays = [date(2024, 6, 17)]
        assert is_business_day(date(2024, 6, 17), holidays) is False


class TestAddBusinessDays:
    def test_add_one(self) -> None:
        # Friday + 1 = Monday
        assert add_business_days(date(2024, 6, 14), 1) == date(2024, 6, 17)

    def test_add_five(self) -> None:
        # Monday + 5 = next Monday
        assert add_business_days(date(2024, 6, 17), 5) == date(2024, 6, 24)

    def test_add_zero(self) -> None:
        d = date(2024, 6, 17)
        assert add_business_days(d, 0) is d

    def test_subtract_one(self) -> None:
        # Monday - 1 = previous Friday
        assert add_business_days(date(2024, 6, 17), -1) == date(2024, 6, 14)

    def test_with_holidays(self) -> None:
        holidays = [date(2024, 6, 17)]  # Monday is holiday
        # Friday + 1, skip Monday holiday = Tuesday
        assert add_business_days(date(2024, 6, 14), 1, holidays) == date(2024, 6, 18)


class TestBusinessDaysBetween:
    def test_same_week(self) -> None:
        # Mon to Fri = 4 business days
        assert business_days_between(date(2024, 6, 17), date(2024, 6, 21)) == 4

    def test_across_weekend(self) -> None:
        # Fri to next Mon = 1 business day
        assert business_days_between(date(2024, 6, 14), date(2024, 6, 17)) == 1

    def test_same_day(self) -> None:
        assert business_days_between(date(2024, 6, 17), date(2024, 6, 17)) == 0

    def test_start_after_end(self) -> None:
        assert business_days_between(date(2024, 6, 20), date(2024, 6, 17)) == 0

    def test_with_holidays(self) -> None:
        holidays = [date(2024, 6, 18)]
        # Mon to Fri, minus Tuesday holiday = 3
        assert business_days_between(date(2024, 6, 17), date(2024, 6, 21), holidays) == 3


class TestRelativeString:
    def test_today(self) -> None:
        d = date(2024, 6, 15)
        assert to_relative_string(d, today=d) == "today"

    def test_tomorrow(self) -> None:
        assert to_relative_string(date(2024, 6, 16), today=date(2024, 6, 15)) == "tomorrow"

    def test_yesterday(self) -> None:
        assert to_relative_string(date(2024, 6, 14), today=date(2024, 6, 15)) == "yesterday"

    def test_days_ago(self) -> None:
        assert to_relative_string(date(2024, 6, 12), today=date(2024, 6, 15)) == "3 days ago"

    def test_days_future(self) -> None:
        assert to_relative_string(date(2024, 6, 18), today=date(2024, 6, 15)) == "in 3 days"

    def test_weeks(self) -> None:
        assert to_relative_string(date(2024, 5, 25), today=date(2024, 6, 15)) == "3 weeks ago"

    def test_months(self) -> None:
        assert to_relative_string(date(2024, 3, 15), today=date(2024, 6, 15)) == "3 months ago"

    def test_years(self) -> None:
        assert to_relative_string(date(2022, 6, 15), today=date(2024, 6, 15)) == "2 years ago"

    def test_1_week(self) -> None:
        assert to_relative_string(date(2024, 6, 22), today=date(2024, 6, 15)) == "in 1 week"

    def test_1_month(self) -> None:
        assert to_relative_string(date(2024, 7, 15), today=date(2024, 6, 15)) == "in 1 month"

    def test_1_year(self) -> None:
        assert to_relative_string(date(2025, 6, 15), today=date(2024, 6, 15)) == "in 1 year"


class TestAge:
    def test_basic(self) -> None:
        assert age(date(1990, 6, 15), today=date(2024, 6, 15)) == 34

    def test_before_birthday(self) -> None:
        assert age(date(1990, 6, 15), today=date(2024, 6, 14)) == 33

    def test_after_birthday(self) -> None:
        assert age(date(1990, 6, 15), today=date(2024, 6, 16)) == 34


class TestFiscalQuarter:
    def test_calendar_year(self) -> None:
        assert fiscal_quarter(date(2024, 1, 15)) == 1
        assert fiscal_quarter(date(2024, 4, 15)) == 2
        assert fiscal_quarter(date(2024, 7, 15)) == 3
        assert fiscal_quarter(date(2024, 10, 15)) == 4

    def test_fiscal_year_july(self) -> None:
        assert fiscal_quarter(date(2024, 7, 15), start_month=7) == 1
        assert fiscal_quarter(date(2024, 10, 15), start_month=7) == 2
        assert fiscal_quarter(date(2025, 1, 15), start_month=7) == 3
        assert fiscal_quarter(date(2025, 4, 15), start_month=7) == 4


class TestFiscalYear:
    def test_calendar_year(self) -> None:
        assert fiscal_year(date(2024, 6, 15)) == 2024

    def test_fiscal_year_july(self) -> None:
        assert fiscal_year(date(2024, 7, 15), start_month=7) == 2024
        assert fiscal_year(date(2024, 6, 15), start_month=7) == 2023


class TestNextPrevBusinessDay:
    def test_next_from_friday(self) -> None:
        assert next_business_day(date(2024, 6, 14)) == date(2024, 6, 17)

    def test_previous_from_monday(self) -> None:
        assert previous_business_day(date(2024, 6, 17)) == date(2024, 6, 14)
