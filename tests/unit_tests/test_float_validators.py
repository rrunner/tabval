"""Unit tests of float validator functions."""

# ruff: noqa: PT011
from contextlib import nullcontext

import pytest

from src.utils.exceptions import InvalidArgumentError
from src.validators.float_validators import significant_decimals


@pytest.mark.parametrize(
    ("number", "expectation"),
    [
        (3.14, 2),
        (0.10, 1),
        (0, 0),
        (100, 0),
        (28.001, 3),
        (28302982.39393929, 8),
        (-192993.3993, 4),
        (-0.0000322, 7),
    ],
)
def test_significant_decimals(number: float, expectation: int) -> None:
    """Test the number of significant number of decimals."""
    assert significant_decimals(number) == expectation, (
        "wrong number of significant decimals"
    )


@pytest.mark.parametrize(
    ("number", "max_allowed", "expectation"),
    [
        (3.14, 2, nullcontext()),
        (0.10, 2, nullcontext()),
        (28.001, 2, pytest.raises(ValueError)),
        (28302982.39393929, 5, pytest.raises(ValueError)),
        (3.14, -1, pytest.raises(InvalidArgumentError)),
    ],
)
def test_significant_decimals_raises(
    number: float,
    max_allowed: int,
    expectation: nullcontext,
) -> None:
    """Test that significant_decimals raises ValueError."""
    with expectation:
        significant_decimals(number, max_allowed)
