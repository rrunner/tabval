"""Validator functions for integers.

To be used in before/after validators in a Pydantic model.

Raise all exceptions as ValueError to ensure Pydantic raises ValidationError.
"""


def is_even(number: int) -> int:
    """Is number even divisible by 2.

    Args:
        number: an integer

    Returns:
        the number if even


    Raises:
        ValueError: when number is not even

    """
    if number % 2 != 0:
        msg = "Integer is not even"
        raise ValueError(msg)
    return number
