"""Create a report using context manager protocol."""

import itertools
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Self
from zoneinfo import ZoneInfo

from markdownmaker.document import Document
from markdownmaker.markdownmaker import (
    Header,
    HeaderSubLevel,
    HorizontalRule,
    InlineCode,
    Paragraph,
)
from pydantic import ValidationError
from tabulate import tabulate

if TYPE_CHECKING:
    from collections.abc import Iterator
    from types import TracebackType

    from src.utils.interface import Tabular


@dataclass(frozen=True, kw_only=True, slots=True)
class Error:
    """Contain a single validation error in source data.

    A single row in the tabular data source may be subject to multiple
    validation errors. An instance of this class will contain the relevant
    attributes for each validation error in source data.

    Attributes:
        loc: field/column with the validation error
        msg: error message
        input: the input that caused the error

    """

    row_id: int
    loc: str
    msg: str
    input: str


class Report:
    """Report class."""

    def __init__(
        self,
        tabular: Tabular,
        output_file: str | Path,
        n_each_error_type: int = 1,
    ) -> None:
        """Init method.

        Args:
            tabular: tabular data object
            output_file: persist markdown report to path output_file (only
            stores report when some rows are validated)
            n_each_error_type: number of individual errors to be listed of each
            error type in the report

        """
        self.tabular = tabular
        self.n_each_error_type = n_each_error_type
        self.num_rows_validated = 0
        self.num_rows_with_errors = 0
        self.total_number_of_errors = 0
        self.errors: list[Error] = []
        self.md_report = Document()
        self.output_file = (
            output_file if isinstance(output_file, Path) else Path(output_file)
        )

    def __enter__(self) -> Self:
        """Enter method.

        Returns:
            the instance itself

        """
        return self

    def create_report(self) -> None:
        """Create report.

        Perform data validation and create a markdown report.
        """
        self.md_report.add(Header("Validation Report\n"))
        with HeaderSubLevel(self.md_report):
            self.md_report.add(Header("Key Figures\n"))
            self.md_report.add(HorizontalRule())
            self.md_report.add(
                Paragraph(
                    f"Data source description: {InlineCode(self.tabular.src_description)}\n"
                    f"Pydantic model: {InlineCode(self.tabular.model.__name__)}\n"  # ty:ignore[unresolved-attribute]
                    f"Report created: {InlineCode(datetime.now(tz=ZoneInfo('UTC')).isoformat(timespec='seconds'))}",
                ),
            )
            self._validate_rows()
            self.md_report.add(
                Paragraph(
                    f"Total number of rows validated: {InlineCode(str(self.num_rows_validated))}\n"
                    f"Total number of rows with errors: {InlineCode(str(self.num_rows_with_errors))}\n"
                    f"Total number of errors: {InlineCode(str(self.total_number_of_errors))}",
                ),
            )
            if self.total_number_of_errors == 0:
                return
        with HeaderSubLevel(self.md_report):
            self.md_report.add(Header("Frequency List\n"))
            self.md_report.add(HorizontalRule())
            freq_list = self.produce_freq_list()
            headers = ["Error type", "Frequency"]
            self.md_report.add(
                Paragraph(tabulate(freq_list, headers=headers, tablefmt="pipe")),
            )
        with HeaderSubLevel(self.md_report):
            self.md_report.add(
                Header(f"Error type: {self.n_each_error_type} of each error type\n"),
            )
            self.md_report.add(HorizontalRule())
            error_coll = self.select_n_of_each_error()
            headers = ["Row ID", "Column", "Error message", "Input value"]
            for individual_errors in error_coll.values():
                with HeaderSubLevel(self.md_report):
                    self.md_report.add(
                        Paragraph(
                            tabulate(
                                individual_errors,
                                headers=headers,
                                tablefmt="pipe",
                            ),
                        ),
                    )

    def _validate_rows(self) -> None:
        """Validate data and produce an Error instance for each error."""
        for row in self.tabular.parse_data():
            self.num_rows_validated += 1
            try:
                self.tabular.model.model_validate(row)
            except ValidationError as ex:
                self.num_rows_with_errors += 1
                self.total_number_of_errors += ex.error_count()
                for error in ex.errors(include_context=False, include_url=False):
                    single_error = Error(
                        row_id=self.num_rows_validated,
                        loc=", ".join(error.get("loc", "")),  # ty:ignore[no-matching-overload]
                        msg=error.get("msg"),
                        input=error.get("input"),
                    )
                    self.errors.append(single_error)

    def _create_groups(self) -> Iterator:
        """Support method.

        Sorts and group wrt. error types

        Returns:
           an iterator

        """
        errors_sorted = sorted(self.errors, key=lambda x: x.msg)
        grouped = itertools.groupby(errors_sorted, key=lambda x: x.msg)
        return grouped

    def produce_freq_list(self) -> list:
        """Produce a frequency list of each error type in descending order."""
        grouped = self._create_groups()
        freq_list = (
            (error_type, len(list(individual_errors_iter)))
            for error_type, individual_errors_iter in grouped
        )
        freq_list_desc = sorted(freq_list, key=lambda x: x[1], reverse=True)
        return freq_list_desc

    def select_n_of_each_error(self) -> dict[str, list]:
        """Select N examples of each error type."""
        grouped = self._create_groups()
        error_coll = defaultdict(list)
        for error_type, individual_errors_iter in grouped:
            for individual_error in itertools.islice(
                individual_errors_iter,
                self.n_each_error_type,
            ):
                error_coll[error_type].append(individual_error)
        return error_coll

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        """Exit method (teardown).

        Store markdown report if any rows have been validated.

        Args:
            exc_type: exception traceback type
            exc_value: exception value
            exc_tb: traceback

        """
        if self.num_rows_validated:
            with Path.open(self.output_file, "w") as f:
                f.write(self.md_report.write())
        # any exception is raised by the with statement
        return False
