"""User defined (annotated) types."""

from datetime import datetime
from enum import StrEnum
from typing import Annotated

from pydantic import (
    AfterValidator,
    BeforeValidator,
    FutureDatetime,
    PastDatetime,
)

from src.validators.common_validators import cast_value
from src.validators.date_validators import make_utc, parse_date
from src.validators.float_validators import significant_decimals
from src.validators.int_validators import is_even

DateUTC = Annotated[datetime, BeforeValidator(parse_date), AfterValidator(make_utc)]

CastToIntNone = Annotated[
    int | None,
    BeforeValidator(
        lambda value, cast_to=int: cast_value(value, cast_to),
    ),
]

CastToFloatNone = Annotated[
    float | None,
    BeforeValidator(lambda value, cast_to=float: cast_value(value, cast_to)),
]

# parser convert empty strings to None (FutureDatetime don't accept None)
FutureDateUTC = Annotated[
    FutureDatetime | None,
    BeforeValidator(parse_date),
    AfterValidator(make_utc),
]

# parser convert empty strings to None (PastDatetime don't accept None)
PastDateUTC = Annotated[
    PastDatetime | None,
    BeforeValidator(parse_date),
    AfterValidator(make_utc),
]

FloatMaxTwoDecimals = Annotated[
    float,
    AfterValidator(
        lambda number, max_allowed=2: significant_decimals(number, max_allowed),
    ),
]

EvenIntConstr = Annotated[int, AfterValidator(is_even)]


class Status(StrEnum):
    """Status enum.

    Attributes:
        PENDING: pending status
        CANCELLED: cancelled status
        DECLINED: declined status
        APPROVED: approved status

    """

    PENDING = "Pending"
    CANCELLED = "Cancelled"
    DECLINED = "Declined"
    APPROVED = "Approved"
