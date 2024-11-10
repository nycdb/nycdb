#!/usr/bin/env python3
"""
    This script makes it easy to create scaffolding for a new
    NYC-DB dataset based on an input CSV file. Just copy it
    into the `/src` directory of your NYC-DB repository,
    open a terminal and run e.g.:

        python create_dataset.py my_data.csv

    This will create all the data files and Python code needed
    for a new dataset called 'my_data' (or whatever you named
    your file).

    The scaffolding is just a starting point,
    however, and you will likely need to tweak things
    before submitting a pull request.

    ## Undoing things

    If you ran the tool by mistake or something, run e.g.:

        python create_dataset.py my_data.csv --undo

    This will remove all files that were created and
    un-modify all files that were modified (assuming you
    haven't already changed them).

    ## Testing

    The script comes with a self-test which creates a simple
    temporary CSV file, runs itself on the CSV, runs the
    integration test it created for the new dataset, and
    then undoes everything it just did.

    To run the self-test, do:

        python create_dataset.py test
"""

import sys
import re
import csv
import random
import argparse
import textwrap
import subprocess
from pathlib import Path


SRC_DIR = Path(__file__).parent.parent.resolve()
NYCDB_DIR = SRC_DIR / "nycdb"
DATASETS_DIR = NYCDB_DIR / "datasets"
TRANSFORMATIONS_PY_PATH = NYCDB_DIR / "dataset_transformations.py"
SQL_DIR = NYCDB_DIR / "sql"
TEST_DIR = SRC_DIR / "tests" / "integration"
NYCDB_TEST_PY_PATH = TEST_DIR / "test_nycdb.py"
TEST_DATA_DIR = TEST_DIR / "data"

assert DATASETS_DIR.exists()
assert TRANSFORMATIONS_PY_PATH.exists()
assert SQL_DIR.exists()
assert TEST_DIR.exists()
assert NYCDB_TEST_PY_PATH.exists()
assert TEST_DATA_DIR.exists()


class DatasetCreator:
    def __init__(
        self,
        name: str,
        yaml_code: str,
        transform_py_code: str,
        sql_code: str,
        test_py_code: str,
        test_csv_text: str,
    ) -> None:
        self.name = name
        self.yaml_code = yaml_code
        self.transform_py_code = transform_py_code
        self.sql_code = sql_code
        self.test_py_code = test_py_code
        self.test_csv_text = test_csv_text

        self.yaml_path = DATASETS_DIR / f"{name}.yml"
        self.sql_path = SQL_DIR / f"{name}.sql"
        self.test_csv_path = TEST_DATA_DIR / f"{name}.csv"

    def append_to_file(self, path: Path, text: str) -> None:
        with path.open("a") as f:
            print(f"Appending to {self.relpath(path)}.")
            f.write(self._with_leading_newlines(text))

    def unappend_from_file(self, path: Path, text: str) -> None:
        to_remove = self._with_leading_newlines(text)
        curr_text = path.read_text()
        if to_remove in curr_text:
            print(f"Undoing changes to {self.relpath(path)}.")
            path.write_text(curr_text.replace(to_remove, ""))

    def _with_leading_newlines(self, text: str) -> str:
        return f"\n\n{text}"

    def create_file(self, path: Path, text: str) -> None:
        print(f"Creating {self.relpath(path)}.")
        path.write_text(text)

    def relpath(self, path: Path) -> str:
        return str(path.relative_to(SRC_DIR))

    def execute(self) -> None:
        self.undo()
        self.create_file(self.yaml_path, self.yaml_code)
        self.create_file(self.sql_path, self.sql_code)
        self.create_file(self.test_csv_path, self.test_csv_text)
        self.append_to_file(TRANSFORMATIONS_PY_PATH, self.transform_py_code)
        self.append_to_file(NYCDB_TEST_PY_PATH, self.test_py_code)

    def undo(self) -> None:
        paths = [self.yaml_path, self.sql_path, self.test_csv_path]
        for path in paths:
            if path.exists():
                print(f"Removing {self.relpath(path)}.")
                path.unlink()
        self.unappend_from_file(TRANSFORMATIONS_PY_PATH, self.transform_py_code)
        self.unappend_from_file(NYCDB_TEST_PY_PATH, self.test_py_code)


def is_valid_identifier(path: str) -> bool:
    """
    Returns whether the argument is a valid Python identifier
    that starts with an alphabetic character or an underscore
    and contains only alphanumeric characters or underscores
    thereafter, e.g.:

        >>> is_valid_identifier('boop')
        True
        >>> is_valid_identifier('0boop')
        False
        >>> is_valid_identifier('_boop')
        True
        >>> is_valid_identifier('@#$@!#$')
        False
    """

    return bool(re.match(r"^[A-Za-z_][A-Za-z0-9_]+$", path))


# https://stackoverflow.com/a/19053800
def to_pascal_case(snake_str: str) -> str:
    """
    Convert the given string to pascal case, e.g.:

        >>> to_pascal_case('boop_bap')
        'BoopBap'
    """

    components = snake_str.replace(" ", "_").split("_")
    return "".join(x.title() for x in components)


def cleanup_text(text: str) -> str:
    return textwrap.dedent(text).lstrip()


def get_head(filepath: Path, max_lines: int) -> str:
    lines = []
    i = 0
    with filepath.open("r") as f:
        for line in f.readlines():
            lines.append(line)
            i += 1
            if i >= max_lines:
                break
    return "".join(lines)


def guess_data_type(name: str, value: str) -> str:
    """
    Returns the best guess at the SQL datatype that should be used in the YAML
    file based on the column names (for special cases like BBL) and the values
    from the CSV, and defaults to 'text' when there's no better guess.

        >>> guess_data_type('bbl', '1012340123)
        'char(10)'
        >>> guess_data_type('latitude', '43.5123')
        'numeric'
        >>> guess_data_type('unitsres', '10')
        'integer'
        >>> guess_data_type('description', 'illegal conversion')
        'text'
    """
    if name.lower() == "bbl":
        return "char(10)"
    elif name.lower() == "bin":
        return "char(7)"
    elif name.lower() in ["zip", "zipcode", "postalcode", "postcode"]:
        return "char(5)"
    elif value.isnumeric():
        return "integer"

    try:
        float(value)
    except ValueError:
        return "text"
    else:
        return "numeric"


def generate_yaml_code(dataset: str, csvpath: Path) -> str:
    with csvpath.open("r") as f:
        reader = csv.reader(f)
        header_row = next(reader)
        value_row = next(reader)
    fields = "\n        ".join(
        [
            f"{to_pascal_case(name)}: {guess_data_type(name, value)}"
            for name, value in zip(header_row, value_row)
        ]
    )
    return cleanup_text(
        f"""
    ---
    files:
      -
        # TODO: Change this to a real URL!
        url: https://SOME-DOMAIN.ORG/SOME-PATH/{dataset}.csv
        dest: {dataset}.csv
    sql:
        - {dataset}.sql
    schema:
      table_name: {dataset}
      fields:
        # TODO: The data types for these fields likely aren't ideal!
        {fields}
    """
    )


def generate_transform_py_code(dataset: str) -> str:
    return cleanup_text(
        f"""
    def {dataset}(dataset):
        return to_csv(dataset.files[0].dest)
    """
    )


def generate_test_py_code(dataset: str) -> str:
    return cleanup_text(
        f"""
    def test_{dataset}(conn):
        dataset = nycdb.Dataset('{dataset}', args=ARGS)
        dataset.drop()
        dataset.db_import()
        assert row_count(conn, '{dataset}') > 0
        assert has_one_row(conn, "select 1 where to_regclass('public.{dataset}_bbl_idx') is NOT NULL")
        with conn.cursor(row_factory=dict_row) as curs:
            # TODO: Look at the test data and use a column to select a row of data. eg. with a BBL value
            curs.execute("select * from {dataset} WHERE bbl = 'FILL THIS IN'")
            rec = curs.fetchone()
            assert rec is not None
            # TODO: Use another column from that row to confirm the value. Make sure you are using the correct type
            assert rec['COLUMN GOES HERE'] == 'VALUE GOES HERE'
    """
    )


def generate_sql_code(dataset: str) -> str:
    return cleanup_text(
        f"""
    CREATE INDEX {dataset}_bbl_idx on {dataset} (bbl);
    """
    )


def fail(msg: str) -> None:
    sys.stderr.write(f"{msg}\n")
    sys.exit(1)


def selftest():

    print("Running pytest on myself...")

    subprocess.check_call(["pytest", __file__, "--doctest-modules"])

    print("Creating a temporary CSV and running myself on it...")

    i = random.randint(1, 1500000)
    name = f"temptest_{i}"
    tempcsv = SRC_DIR / f"{name}.csv"
    tempcsv.write_text(
        "\n".join(
            ["foo,bar,bbl", 'a,"hello there",3028850001', 'b,"zz zdoj",4028850001']
        )
    )
    try:
        base_args = ["python", __file__, str(tempcsv)]
        subprocess.check_call(base_args)
        try:
            print("Running the test I created for the new dataset...")
            subprocess.check_call(
                ["pytest", str(NYCDB_TEST_PY_PATH), "-k", name, "-vv"]
            )
        finally:
            subprocess.check_call([*base_args, "--undo"])
    finally:
        tempcsv.unlink()

    print("I seem to be working.")


def main():
    parser = argparse.ArgumentParser(
        description="Create scaffolding for a new NYC-DB dataset."
    )
    parser.add_argument("csvfile", help="The CSV file to base the new dataset on.")
    parser.add_argument(
        "--undo",
        action="store_true",
        help="Attempt to undo the creation of the scaffolding.",
    )
    parser.add_argument(
        "--schema-only",
        action="store_true",
        help="Only print the schema for the csv file without editing and code files.",
    )
    parser.add_argument(
        "--test-data-only",
        action="store_true",
        help="Only create and save test data file for the csv file.",
    )
    args = parser.parse_args()

    if args.csvfile == "test":
        selftest()
        return

    csvpath = Path(args.csvfile)

    if not is_valid_identifier(csvpath.stem):
        fail(
            f"'{csvpath.stem}' can contain only alphanumeric characters/underscores,\n"
            f"and cannot start with a number."
        )

    if not csvpath.exists():
        fail(f"'{csvpath}' does not exist!")

    dc = DatasetCreator(
        name=csvpath.stem,
        yaml_code=generate_yaml_code(csvpath.stem, csvpath),
        transform_py_code=generate_transform_py_code(csvpath.stem),
        sql_code=generate_sql_code(csvpath.stem),
        test_py_code=generate_test_py_code(csvpath.stem),
        test_csv_text=get_head(csvpath, max_lines=101),
    )

    if args.undo:
        print(f"Undoing scaffolding for dataset '{dc.name}'.")
        dc.undo()
    elif args.schema_only:
        print(f"YAML schema for dataset '{dc.name}'.")
        print(dc.yaml_code)
    elif args.test_data_only:
        print(f"Saved test data for for dataset '{dc.name}'.")
        dc.create_file(dc.test_csv_path, dc.test_csv_text)
    else:
        dc.execute()
        print(f"Scaffolding created for new dataset '{dc.name}'.")
        print(f"The scaffolding is just a starting point; you should")
        print(f"inspect all the new/modified files and change them")
        print(f"as needed.")


if __name__ == "__main__":
    main()
