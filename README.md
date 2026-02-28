# Data Validation of Tabular Data

`tabval` performs data validation of tabular data using Pydantic.

## Usage

### Example: CSV File

1. Add CSV file to be tested to `data` folder, e.g. `small.csv`

2. Add the user defined Pydantic model to `src/models/models.py`
   - Possibly add user defined validator functions (including tests) to be used
     in BeforeValidator and AfterValidator (annotated types)
   - Add types and annotated types to the Pydantic model

3. Adjust `tabval.py`
   - Import the relevant Pydantic model from `src/models/models.py`
   - Update the object passed to the `Report` context manager
     - Reference the Pydantic model in `model`
     - Reference the CSV data in `src` as a string (relative path)

4. Perform the validation with uv: `uv run -m tabval`

### Example: Pandas DataFrame

1. Add the user defined Pydantic model to `src/models/models.py`
   - Possibly add user defined validator functions (including tests) to be used
     in BeforeValidator and AfterValidator (annotated types)
   - Add types and annotated types to the Pydantic model

2. Adjust `tabval.py`
   - Import the relevant Pydantic model from `src/models/models.py`
   - Update the object passed to the `Report` context manager
     - Reference the Pydantic model in `model`
     - Reference the in-memory pandas DataFrame in `src`

3. Perform the validation with uv: `uv run -m tabval`

### Testing

Unit and integration testing with `pytest`. Execute tests with `uv run pytest`.

## TO-DO

Add support for other tabular data formats such as Polars and Excel.
