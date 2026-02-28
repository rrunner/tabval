"""Unit tests of common validator functions."""

# ruff: noqa: PT011, ANN401
import math
from contextlib import nullcontext
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import pytest
from numpy.ma import masked

from src.validators.common_validators import any_missing, cast_value


@pytest.mark.parametrize(
    ("value", "cast_to", "missing_value", "expectation"),
    [
        (2, int, None, 2),
        (2.5, int, None, 2),
        (-2.5, int, None, -2),
        (None, int, None, None),
        ("", int, None, None),
        (" ", int, None, None),
        (2, float, None, 2),
        (2.5, float, None, 2.5),
        (-2.5, float, None, -2.5),
        (None, float, None, None),
        ("", float, None, None),
        (" ", float, None, None),
    ],
)
def test_cast_type(
    value: float,
    cast_to: type[int | float],
    missing_value: None,
    expectation: float,
) -> None:
    """Test cast_value function."""
    assert cast_value(value, cast_to, missing_value) == expectation, (
        "wrong expected value for cast_value function"
    )


@pytest.mark.parametrize(
    ("value", "cast_to", "missing_value", "expectation"),
    [
        (2, int, None, nullcontext()),
        (2.5, float, None, nullcontext()),
        (2, str, None, pytest.raises(ValueError)),
        (2, list, None, pytest.raises(ValueError)),
        (2, set, None, pytest.raises(ValueError)),
    ],
)
def test_cast_value_raises(
    value: float,
    cast_to: type[int | float],
    missing_value: None,
    expectation: nullcontext,
) -> None:
    """Test that cast_value function raises ValueError."""
    with expectation:
        cast_value(value, cast_to, missing_value)


@pytest.mark.parametrize(
    ("value", "expectation"),
    [
        ("", nullcontext()),
        (" ", nullcontext()),
        (3.12, nullcontext()),
        (-1, nullcontext()),
        (datetime.now(ZoneInfo("UTC")), nullcontext()),
        (None, pytest.raises(ValueError)),
        (np.nan, pytest.raises(ValueError)),
        (np.datetime64("NaT"), pytest.raises(ValueError)),
        (np.timedelta64("NaT"), pytest.raises(ValueError)),
        (masked, pytest.raises(ValueError)),
        (math.nan, pytest.raises(ValueError)),
        (pd.NA, pytest.raises(ValueError)),
        (pd.NaT, pytest.raises(ValueError)),
    ],
)
def test_any_missing_value(value: Any, expectation: nullcontext) -> None:
    """Test any_missing function."""
    with expectation:
        any_missing(value)
