"""Common validator functions.

To be used as before/after validators in a Pydantic model.

Raise all exceptions as ValueError to ensure Pydantic raises ValidationError.
"""

# ruff: noqa: ANN401
from typing import Any

import pandas as pd
from numpy import ma


def cast_value(
    value: Any,
    cast_to: type[int | float],
    missing_value: Any = None,
) -> float | int | None:
    """Cast value into expected type and set default missing value.

    This is useful as a before-validator function (e.g., with Pydantic when
    reading CSV files), where fields are initially strings, and empty values
    should yield a default (e.g., None) when a numeric type is expected.

    Args:
        value: the input value to cast
        cast_to: the numeric type to cast to
        missing_value: the value to return if casting fails (default is None)

    Returns:
        The cast value of type int or float, or the specified missing_value if
        casting fails.

    Raises:
        ValueError: cast_to type is neither of int or float

    """
    if not issubclass(cast_to, (int, float)):
        msg = "cast_to type must be int or float"
        raise ValueError(msg)  # noqa: TRY004

    if isinstance(value, cast_to):
        return value

    try:
        return cast_to(value)
    except ValueError, TypeError:
        return missing_value


def any_missing(value: Any) -> Any:
    """Validate if value is missing.

    Args:
        value: any value to be validated

    Returns:
        the original value if it is not missing

    Raises:
        ValueError: if the value is missing

    """
    if value is None or pd.isna(value) or value is ma.masked:
        msg = f"Missing value detected: {value!r}"
        raise ValueError(msg)
    return value
