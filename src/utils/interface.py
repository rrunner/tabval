"""Interfaces."""

import csv
from pathlib import Path
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from collections.abc import Iterator

    import pandas as pd
    from pydantic import BaseModel


class Tabular(Protocol):
    """Protocol class to parse tabular data."""

    def __init__(self, model: BaseModel, src: str | pd.DataFrame) -> None:
        """Init method for protocol class.

        Defined to avoid type checker issues.
        """
        self.model = model
        self.src = src
        self.src_description: str = ""

    def parse_data(self) -> Iterator:
        """Parse and yield data row-by-row from source.

        Returns:
            a row of data

        """


class TabularCSV:
    """TabularCSV class to parse (tabular) CSV data.

    TabularCSV conforms to Tabular protocol class.
    """

    def __init__(
        self,
        model: type[BaseModel],
        src: str,
        *,
        skip_header: bool = True,
    ) -> None:
        """Init method.

        Args:
            model: Pydantic model used to validate src
            src: path to CSV file (string)
            skip_header: skip parsing of header

        """
        self.model = model
        self.src = src
        self.skip_header = skip_header
        self.src_description = f"{self.src}"

    def parse_data(self) -> Iterator:
        """Parse and yield data row-by-row from CSV file.

        Yields:
            a row of CSV data (skip header) as a dictionary with names set by
            the Pydantic model

        """
        with Path.open(Path(self.src)) as f:
            data = csv.DictReader(
                f,
                fieldnames=self.model.model_fields.keys(),
            )
            if self.skip_header:
                next(data)
            yield from data


class TabularPandasDF:
    """TabularPandasDF class to parse (tabular) Pandas dataframe data.

    TabularPandasDF conforms to Tabular protocol class.
    """

    def __init__(
        self,
        model: type[BaseModel],
        src: pd.DataFrame,
    ) -> None:
        """Init method.

        Args:
            model: Pydantic model used to validate src
            src: Pandas dataframe

        """
        self.model = model
        self.src = src
        row, column = self.src.shape
        self.src_description = (
            f"{type(self.src).__name__} with {row} rows and {column} columns"
        )

    def parse_data(self) -> Iterator:
        """Parse and yield data row-by-row from a Pandas dataframe.

        Yields:
            a row of Pandas dataframe as a dictionary with names set by the
            Pydantic model

        """
        model_fields = self.model.model_fields.keys()
        for _, row in self.src.iterrows():
            yield dict(zip(model_fields, row.values, strict=True))
