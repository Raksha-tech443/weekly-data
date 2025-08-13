from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, Iterable, Tuple

DATE_FMT = "%Y-%m-%d"

def _parse_date(s: str):
    try:
        return datetime.strptime(s, DATE_FMT).date()
    except ValueError:
        raise ValueError(f"Invalid date format: {s}. Expected YYYY-MM-DD.")

def _monday_of_week(d):
    return d - timedelta(days=d.weekday())  # Monday = 0

def validate_input(data: Dict[str, int]) -> None:
    if not isinstance(data, dict) or not data:
        raise ValueError("Input must be a non-empty dict of {'YYYY-MM-DD': int}.")

    has_monday = False
    has_sunday = False

    for k, v in data.items():
        if not isinstance(k, str):
            raise ValueError("All keys must be date strings.")
        d = _parse_date(k)
        if not (datetime(1970, 1, 1).date() <= d <= datetime(2100, 1, 1).date()):
            raise ValueError(f"Date out of allowed range: {k}")
        if not isinstance(v, int) or not (-1_000_000 <= v <= 1_000_000):
            raise ValueError(f"Value out of allowed range [-1e6, 1e6]: {k} -> {v}")

        wd = d.weekday()
        if wd == 0:
            has_monday = True
        if wd == 6:
            has_sunday = True

    if not has_monday or not has_sunday:
        raise ValueError("Dataset must contain at least one Monday and one Sunday.")

def aggregate_weekly(data: Dict[str, int]) -> Dict[str, int]:
    """
    Groups by Monday–Sunday weeks and sums values.
    Returns dict: { 'YYYY-MM-DD' (Monday of week): total_sum }
    """
    validate_input(data)
    weekly = defaultdict(int)
    for ds, val in data.items():
        d = _parse_date(ds)
        week_monday = _monday_of_week(d)
        weekly[week_monday] += val
    # sort by week start and stringify keys
    return {k.strftime(DATE_FMT): weekly[k] for k in sorted(weekly.keys())}

if __name__ == "__main__":
    # Minimal demo
    sample = {
        "2025-08-11": 10,  # Monday
        "2025-08-12": 20,
        "2025-08-17": 30,  # Sunday
    }
    print(aggregate_weekly(sample))
