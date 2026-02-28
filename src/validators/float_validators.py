"""Validator functions for floats.

To be used in before/after validators in a Pydantic model.

Raise all exceptions as ValueError to ensure Pydantic raises ValidationError.
"""

from decimal import Decimal

from src.utils.exceptions import InvalidArgumentError


def significant_decimals(number: float, max_allowed: int | None = None) -> int:
    """Return the number of significant decimals for a float.

    Note: cast to int to avoid "unary operator not supported" ty error

    Args:
        number: float number
        max_allowed: maximum number of allowed decimals

    Returns:
        number of significant decimals

    """
    if max_allowed and max_allowed < 0:
        msg = "max_allowed must be non-negative"
        raise InvalidArgumentError(msg)
    dec = Decimal(str(number))
    num_decimals = max(-int(dec.as_tuple().exponent), 0)
    if max_allowed and num_decimals > max_allowed:
        msg = "Number of decimals exceed threshold"
        raise ValueError(msg)
    return num_decimals
