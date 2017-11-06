import nycdb
import os

def test_extract_csvs_from_zip():
    test_csv_file = os.path.join(os.path.dirname(__file__), 'cats.zip')
    csv_content = nycdb.transform.extract_csvs_from_zip(test_csv_file)
    result = "name,superpower\nalice,eating\nfluffy,purring\nmeowses,sitting\npickles,looking out the window\n"
    assert csv_content == result
