"""Unit tests of integer validator functions."""

# ruff: noqa: PT011
from contextlib import nullcontext

import pytest

from src.validators.int_validators import is_even


@pytest.mark.parametrize(
    ("number", "expectation"),
    [
        (2, 2),
        (0, 0),
        (-4, -4),
    ],
)
def test_is_even(number: int, expectation: int) -> None:
    """Test is_even function."""
    assert is_even(number) == expectation, "wrong expected value for is_even function"


@pytest.mark.parametrize(
    ("number", "expectation"),
    [
        (2, nullcontext()),
        (-2, nullcontext()),
        (1, pytest.raises(ValueError)),
        (-1, pytest.raises(ValueError)),
    ],
)
def test_is_even_raises(number: int, expectation: nullcontext) -> None:
    """Test that is_even function raises ValueError."""
    with expectation:
        is_even(number)
