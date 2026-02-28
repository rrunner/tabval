"""Unit tests of date validator functions."""

# ruff: noqa: PT011, DTZ001
from contextlib import nullcontext
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from dateutil.tz.tz import tzoffset

from src.validators.date_validators import make_utc, parse_date


@pytest.mark.parametrize(
    ("input_str", "expected"),
    [
        ("July 8, 2001, 08:01 pm", datetime(2001, 7, 8, 20, 1, 0)),
        ("1989-10-02 01:00:04", datetime(1989, 10, 2, 1, 0, 4)),
        (
            "1994-11-05T13:15:30Z",
            datetime(1994, 11, 5, 13, 15, 30, tzinfo=ZoneInfo("UTC")),
        ),
        (
            "1997-07-16T19:20:30+01:00",
            datetime(1997, 7, 16, 19, 20, 30, tzinfo=tzoffset(None, 3600)),
        ),
        (
            datetime(1997, 7, 16, 19, 20, 30),
            datetime(1997, 7, 16, 19, 20, 30),
        ),
        (
            "",
            None,
        ),
    ],
)
def test_parse_date(input_str: str, expected: datetime | None) -> None:
    """Test that parse_date can parse and return datetime-like objects."""
    dt = parse_date(input_str)
    assert dt == expected


@pytest.mark.parametrize(
    ("input_str", "expectation"),
    [
        ("1997-07-16T19:20:30+01:00", nullcontext()),
        ("July 8, 2001, 08:01 pm", nullcontext()),
        (datetime(2020, 2, 23), nullcontext()),
        (None, pytest.raises(ValueError)),
        ("magic date", pytest.raises(ValueError)),
        ("", nullcontext()),
    ],
)
def test_parse_date_raises(input_str: str, expectation: nullcontext) -> None:
    """Test that function raises expected value incl. ValueError."""
    with expectation:
        parse_date(input_str)


@pytest.mark.parametrize(
    ("input_dt", "expected"),
    [
        (
            datetime(2023, 11, 23),
            datetime(2023, 11, 23, 0, 0, 0, tzinfo=ZoneInfo("UTC")),
        ),
        (
            datetime(2023, 11, 23, 0, 0, 0),
            datetime(2023, 11, 23, 0, 0, 0, tzinfo=ZoneInfo("UTC")),
        ),
        (
            datetime(2023, 11, 23, 0, 0, 0, tzinfo=ZoneInfo("Europe/Berlin")),
            datetime(2023, 11, 22, 23, 0, 0, tzinfo=ZoneInfo("UTC")),
        ),
        (
            datetime(2023, 11, 23, 16, 30, 10, tzinfo=ZoneInfo("Australia/Sydney")),
            datetime(2023, 11, 23, 5, 30, 10, tzinfo=ZoneInfo("UTC")),
        ),
        (
            None,
            None,
        ),
    ],
)
def test_make_utc(input_dt: datetime | None, expected: datetime | None) -> None:
    """Test that datetime object is converted to UTC aware datetime object."""
    dt = make_utc(input_dt)
    if dt is None:
        return
    assert dt == expected, "datetime is not the expected UTC datetime"
    assert dt.tzinfo == ZoneInfo("UTC"), "datetime tzinfo is not UTC"
