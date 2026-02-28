"""Main module."""

from data.small import small
from src.models.models import ExampleSmall
from src.utils.interface import TabularPandasDF
from src.utils.report import Report


def validate() -> None:
    """Validate data with Pydantic."""
    with Report(
        TabularPandasDF(
            model=ExampleSmall,
            src=small,
        ),
        output_file="output.md",
    ) as report:
        report.create_report()


if __name__ == "__main__":
    validate()
