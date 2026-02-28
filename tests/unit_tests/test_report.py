"""Unit tests of report."""

from collections import defaultdict
from dataclasses import FrozenInstanceError
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from markdownmaker.markdownmaker import Document

from src.models.models import ExampleSmall, ExampleTest
from src.utils.interface import TabularCSV
from src.utils.report import Error, Report

if TYPE_CHECKING:
    from collections.abc import Callable


def test_creation_error_class() -> None:
    """Test that it is possible to create an instance of the Error class."""
    error = Error(
        row_id=1,
        loc="Column1",
        msg="Some error message",
        input="3",
    )
    assert isinstance(error, Error), "error is not an instance of Error"
    assert error.row_id == 1, "attribute row_id is wrong"
    assert error.loc == "Column1", "attribute loc is wrong"
    assert error.msg == "Some error message", "attribute msg is wrong"
    assert error.input == "3", "attribute input is wrong"


def test_immutable_error_raises() -> None:
    """Test that an exception is raised when mutating an instance of the Error class."""
    error = Error(
        row_id=1,
        loc="Column1",
        msg="Some error message",
        input="3",
    )
    with pytest.raises(FrozenInstanceError):
        error.input = "4"  # ty:ignore[invalid-assignment]


@pytest.mark.parametrize(
    "path",
    ["test.md", Path("test.md")],
)
def test_creation_report(tmp_path: Path, path: str | Path) -> None:
    """Test that to create an instance of the Report class.

    Also verify that the output file that contains the markdown report is created.
    """
    with Report(
        TabularCSV(
            model=ExampleTest,
            src="data/test.csv",
        ),
        output_file=tmp_path / path,
    ) as report:
        report.create_report()
    assert isinstance(report, Report), "report is not an instance of class Report"
    assert report.output_file.exists(), "output file does not exist"


@pytest.mark.parametrize(
    "path",
    ["test.md", Path("test.md")],
)
def test_no_output_if_no_validation(tmp_path: Path, path: str | Path) -> None:
    """Test that the output file is not written if no validation has been performed."""
    with Report(
        TabularCSV(
            model=ExampleTest,
            src="data/test.csv",
        ),
        output_file=tmp_path / path,
    ) as report:
        pass
    assert isinstance(report, Report), "report is not an instance of class Report"
    assert not report.output_file.exists(), "output file exist"


@pytest.fixture
def create_errors(tmp_path: Path) -> Callable:
    """Fixture that returns a function.

    The _wrapper returns a Report instance prepared with errors.
    """

    def _wrapper(n: int) -> Report:
        report = Report(
            TabularCSV(
                model=ExampleTest,
                src="data/test.csv",
            ),
            output_file=tmp_path / "test.md",
            n_each_error_type=n,
        )
        report.errors = [
            Error(row_id=1, loc="var1", msg="error1", input="1"),
            Error(row_id=2, loc="var1", msg="error1", input="1"),
            Error(row_id=3, loc="var1", msg="error1", input="1"),
            Error(row_id=1, loc="var2", msg="error2", input="2"),
            Error(row_id=2, loc="var2", msg="error2", input="2"),
            Error(row_id=3, loc="var3", msg="error3", input="3"),
        ]
        return report

    return _wrapper


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (1, [("error1", 3), ("error2", 2), ("error3", 1)]),
        (2, [("error1", 3), ("error2", 2), ("error3", 1)]),
        (5, [("error1", 3), ("error2", 2), ("error3", 1)]),
    ],
)
def test_freq_list(
    create_errors: Callable,
    n: int,
    expected: list[tuple[str, int]],
) -> None:
    """Test produce_freq_list method (expected result does not vary with n)."""
    grouped_count_desc = create_errors(n=n).produce_freq_list()
    assert grouped_count_desc == expected


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (
            1,
            defaultdict(
                error1=[Error(row_id=1, loc="var1", msg="error1", input="1")],
                error2=[Error(row_id=1, loc="var2", msg="error2", input="2")],
                error3=[Error(row_id=3, loc="var3", msg="error3", input="3")],
            ),
        ),
        (
            2,
            defaultdict(
                error1=[
                    Error(row_id=1, loc="var1", msg="error1", input="1"),
                    Error(row_id=2, loc="var1", msg="error1", input="1"),
                ],
                error2=[
                    Error(row_id=1, loc="var2", msg="error2", input="2"),
                    Error(row_id=2, loc="var2", msg="error2", input="2"),
                ],
                error3=[Error(row_id=3, loc="var3", msg="error3", input="3")],
            ),
        ),
        (
            3,
            defaultdict(
                error1=[
                    Error(row_id=1, loc="var1", msg="error1", input="1"),
                    Error(row_id=2, loc="var1", msg="error1", input="1"),
                    Error(row_id=3, loc="var1", msg="error1", input="1"),
                ],
                error2=[
                    Error(row_id=1, loc="var2", msg="error2", input="2"),
                    Error(row_id=2, loc="var2", msg="error2", input="2"),
                ],
                error3=[Error(row_id=3, loc="var3", msg="error3", input="3")],
            ),
        ),
    ],
)
def test_select_n_of_each_error(
    create_errors: Callable,
    n: int,
    expected: dict[str, list],
) -> None:
    """Test select_n_of_each_error method (expected result vary with n)."""
    error_coll = create_errors(n=n).select_n_of_each_error()
    assert error_coll == expected


def test_create_report(create_errors: Callable, tmp_path: Path) -> None:
    """Test that create_report method can produce a report in markdown."""
    report = create_errors(n=1)
    report.create_report()
    assert isinstance(report.md_report, Document)


def test_create_report_wo_errors(tmp_path: Path) -> None:
    """Test that create_report method can produce a report in markdown when there are no errors."""
    report = Report(
        TabularCSV(
            model=ExampleSmall,
            src="data/small.csv",
        ),
        output_file=tmp_path / "test.md",
    )
    report.create_report()
    assert isinstance(report.md_report, Document)
