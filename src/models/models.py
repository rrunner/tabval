"""Pydantic models."""

from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,  # noqa: TC002
    field_validator,
)

from .annotated_types import (  # noqa: TC001
    CastToFloatNone,
    CastToIntNone,
    DateUTC,
    EvenIntConstr,
    FloatMaxTwoDecimals,
    FutureDateUTC,
    PastDateUTC,
    Status,
)


class ExampleSmall(BaseModel):
    """Pydantic model that corresponds to small test data."""

    id: int
    name: str


class ExampleTest(BaseModel):
    """Pydantic model that corresponds to larger test data."""

    model_config = ConfigDict(
        strict=False,
        str_strip_whitespace=True,
        validate_assignment=True,
        validate_default=True,
    )

    date: DateUTC = Field(
        ge=datetime(1980, 1, 1, tzinfo=ZoneInfo("UTC")),
        le=datetime(2030, 1, 1, tzinfo=ZoneInfo("UTC")),
    )
    some_int: CastToIntNone
    future_date: FutureDateUTC
    past_date: PastDateUTC
    amount: CastToFloatNone
    float_pos_amount: FloatMaxTwoDecimals = Field(gt=0)
    constr_int: EvenIntConstr = Field(gt=10, lt=20, multiple_of=4)
    status: Status
    payed_amount: float | None

    @field_validator("payed_amount", mode="after")
    @classmethod
    def val_payed_amount_wrt_status(
        cls,
        payed_amount: float | None,
        info: ValidationInfo,
    ) -> float | None:
        """Validate that payed_amount is non-zero for not approved applications."""
        data = info.data
        if payed_amount is None:
            return None
        if "status" in data and payed_amount != 0 and data["status"] != Status.APPROVED:
            msg = f"Field payed_amount is different from 0 when status is {data['status']}"
            raise ValueError(msg)
        return payed_amount
