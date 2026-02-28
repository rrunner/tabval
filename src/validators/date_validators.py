"""Validator functions for dates.

To be used as before/after validators in a Pydantic model.

Raise all exceptions as ValueError to ensure Pydantic raises ValidationError.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from dateutil.parser import parse


def parse_date(date: str | datetime) -> datetime | None:
    """Parse input `date` and try to convert to datetime.

    Args:
        date: datetime-like string

    Returns:
        datetime object (None if empty string is passed)

    Raises:
        ValueError: parser fails to compute a datetime object

    """
    if isinstance(date, datetime):
        return date
    if isinstance(date, str):
        if not date:
            return None
        try:
            dt = parse(date)
        except Exception as ex:
            msg = "Cannot parse date as string"
            raise ValueError(msg) from ex
        return dt
    msg = "Missing value"
    raise ValueError(msg) from None


def make_utc(date: datetime | None) -> datetime | None:
    """Convert datetime object to UTC.

    Set UTC timezone for timezone naive objects, and change to UTC timezone for
    timezone aware objects.

    Args:
        date: datetime object (naive or aware) or None

    Returns:
       UTC adjusted datetime object (None if None is passed)

    """
    if date is None:
        return None
    if date.tzinfo is not None:
        return date.astimezone(tz=ZoneInfo("UTC"))
    return date.replace(tzinfo=ZoneInfo("UTC"))
