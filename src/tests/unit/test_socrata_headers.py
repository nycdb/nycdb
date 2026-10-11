"""
NYC Open Data's SODA3 query.csv export names columns by API field name and
adds system columns such as ":id", where the SODA1 rows.csv export used
display names. For every dataset file downloaded from Socrata, the loader must
produce the same columns from either header.

socrata_headers.json holds the header line of both exports for each file,
captured in October 2026 (one, acris_real_property_parties.csv, was rebuilt
from the dataset's column metadata because both exports timed out).
"""
import csv
import json
import os
from types import SimpleNamespace

import pytest

import nycdb

with open(os.path.join(os.path.dirname(__file__), 'socrata_headers.json'), encoding='utf-8') as f:
    HEADERS = json.load(f)


def loaded_columns(root_dir, dataset_name, dest, table, header):
    """Columns of the first row the loader yields for a file with this header."""
    with open(os.path.join(root_dir, dest), 'w', encoding='utf-8', newline='') as f:
        f.write(header + '\n')
        csv.writer(f).writerow(['1'] * len(next(csv.reader([header]))))
    dataset = nycdb.Dataset(dataset_name, args=SimpleNamespace(root_dir=str(root_dir), hide_progress=True))
    schema = next(s for s in dataset.schemas if s['table_name'] == table)
    return set(next(dataset.transform(schema)))


@pytest.mark.parametrize('key', sorted(HEADERS))
def test_query_csv_loads_same_columns_as_rows_csv(tmpdir, key):
    dataset_name, dest = key.split('/')
    entry = HEADERS[key]
    rows_csv = loaded_columns(tmpdir.mkdir('rows'), dataset_name, dest, entry['table'], entry['rows_csv'])
    query_csv = loaded_columns(tmpdir.mkdir('query'), dataset_name, dest, entry['table'], entry['query_csv'])
    assert query_csv == rows_csv
