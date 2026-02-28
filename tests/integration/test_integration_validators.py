"""Integration tests of validator functions.

Tests are executed in the context of Pydantic model validation, using different
types of data sources.
"""

from typing import TYPE_CHECKING

import pytest
from pydantic import ValidationError

from data.small import small
from data.test import test
from src.models.models import ExampleSmall, ExampleTest
from src.utils.interface import TabularCSV, TabularPandasDF

if TYPE_CHECKING:
    from pydantic import BaseModel

    from src.utils.interface import Tabular


@pytest.mark.parametrize(
    ("tabular", "exp_pydantic_model", "exp_validation_errors"),
    [
        (
            TabularCSV(model=ExampleTest, src="data/test.csv"),
            ExampleTest,
            12,
        ),
        (
            TabularCSV(model=ExampleSmall, src="data/small.csv", skip_header=True),
            ExampleSmall,
            0,
        ),
        (
            TabularPandasDF(model=ExampleSmall, src=small),
            ExampleSmall,
            0,
        ),
        (
            TabularPandasDF(model=ExampleTest, src=test),
            ExampleTest,
            26,
        ),
    ],
)
def test_models(
    tabular: Tabular,
    exp_pydantic_model: type[BaseModel],
    exp_validation_errors: int,
) -> None:
    """Test different Pydantic models with different data inputs.

    Test that the model can deserialize/validate data, and that the model
    raises ValidationError, and that all errors are aggregated properly by
    error_count().

    Note: If any of the Pydantic validators, e.g., built-in validators provided
    by type hints and Field(), raises an ValidationError, any issue found in
    the AfterValidator for the same field (and row) is not raised and included
    in the total count of errors found.
    """
    validation_error = 0
    tabular_object = tabular
    for row in tabular_object.parse_data():
        try:
            result = tabular_object.model.model_validate(row)
        except ValidationError as ex:
            validation_error += ex.error_count()
        else:
            assert isinstance(result, exp_pydantic_model)
    assert validation_error == exp_validation_errors, (
        "Wrong number of ValidationError raised"
    )
