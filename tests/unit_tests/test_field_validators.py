"""Unit tests of field validators class methods."""

# ruff: noqa: PT011
from contextlib import nullcontext
from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest
from pydantic import ValidationInfo

from src.models.models import ExampleTest

if TYPE_CHECKING:
    from collections.abc import Callable

    from src.models.annotated_types import Status


@pytest.fixture
def val_info() -> Callable:
    """Mock ValidationInfo object to a specific status."""

    def _val_info(status: Status) -> Mock:
        mock_info = Mock(spec=ValidationInfo)
        mock_info.data = {"status": status}
        return mock_info

    return _val_info


@pytest.mark.parametrize(
    ("payed_amount", "expectation"),
    [
        (100, 100),
        (0, 0),
        (-100, -100),
        (None, None),
    ],
)
def test_val_payed_amount_wrt_status_approved(
    payed_amount: float | None,
    expectation: float | None,
    val_info: Callable,
) -> None:
    """Test field validator class method."""
    res = ExampleTest.val_payed_amount_wrt_status(
        payed_amount,
        val_info("Approved"),
    )
    assert res == expectation


@pytest.mark.parametrize(
    ("payed_amount", "expectation"),
    [
        (100, pytest.raises(ValueError)),
        (0, nullcontext()),
        (-100, pytest.raises(ValueError)),
        (None, nullcontext()),
    ],
)
def test_val_payed_amount_wrt_status_declined(
    payed_amount: float | None,
    expectation: nullcontext,
    val_info: Callable,
) -> None:
    """Test field validator class method."""
    with expectation:
        ExampleTest.val_payed_amount_wrt_status(payed_amount, val_info("Declined"))
