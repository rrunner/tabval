"""Unit tests of interface."""

from src.models.models import ExampleTest
from src.utils.interface import TabularCSV


def test_create_tabular_instances() -> None:
    """Test to create instances that conforms to the Tabular protocol."""
    model_parser = TabularCSV(
        model=ExampleTest,
        src="data/test.csv",
    )
    assert isinstance(model_parser, TabularCSV), (
        "model_parser object is not an instance of TabularCSV"
    )
    assert issubclass(model_parser.model, ExampleTest), (
        "model object is not a subclass of CSVModel"
    )
    assert hasattr(model_parser, "__init__"), (
        "model_parser does not have an init method"
    )
    assert hasattr(model_parser, "parse_data"), (
        "model_parser does not have a parse_data method"
    )
