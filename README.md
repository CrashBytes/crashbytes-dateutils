# crashbytes-dateutils

Zero-dependency datetime business helpers — business days, fiscal quarters, relative strings.

## Install

```bash
pip install crashbytes-dateutils
```

## Usage

```python
from datetime import date
from crashbytes_dateutils import (
    add_business_days, business_days_between, to_relative_string,
    fiscal_quarter, age, start_of_month, end_of_month,
)

add_business_days(date(2024, 6, 14), 1)           # date(2024, 6, 17) — skips weekend
business_days_between(date(2024, 6, 17), date(2024, 6, 21))  # 4
to_relative_string(date(2024, 6, 12), today=date(2024, 6, 15))  # "3 days ago"
fiscal_quarter(date(2024, 7, 15), start_month=7)   # 1
age(date(1990, 6, 15), today=date(2024, 6, 15))    # 34
```

## License

MIT
