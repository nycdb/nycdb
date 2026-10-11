import nycdb
import os


def test_extract_csvs_from_zip():
    test_csv_file = os.path.join(os.path.dirname(__file__), 'cats.zip')
    csv_content = nycdb.transform.extract_csvs_from_zip(test_csv_file)
    result = ["name,superpower\n", "alice,eating\n", "fluffy,purring\n",
              "meowses,sitting\n", "pickles,looking out the window\n"]
    assert list(csv_content) == result


def test_to_csv(tmpdir):
    f = tmpdir.join('test.csv')
    f.write("name,borough,block,lot\nalice,queens,1,2\nbob,bronx,3,4")

    output_list = list(nycdb.transform.to_csv(f.strpath))
    assert output_list[0] == {'name': 'alice', 'borough': 'queens', 'block': '1', 'lot': '2'}
    assert output_list[1] == {'name': 'bob', 'borough': 'bronx', 'block': '3', 'lot': '4'}


def test_to_csv_drops_socrata_system_columns(tmpdir):
    f = tmpdir.join('test.csv')
    f.write('":id","violation_id","boro",":updated_at"\n'
            '"row-ab12","1","BRONX","2026-10-08T20:07:34.263Z"\n')

    output_list = list(nycdb.transform.to_csv(f.strpath, header_replacements={'boro': 'borough'}))
    assert output_list == [{'violationid': '1', 'borough': 'BRONX'}]


def test_to_csv_system_column_does_not_replace_data_column(tmpdir):
    f = tmpdir.join('test.csv')
    f.write('"id","name",":id"\n"7","alice","row-ab12"\n')

    output_list = list(nycdb.transform.to_csv(f.strpath))
    assert output_list == [{'id': '7', 'name': 'alice'}]


def test_zip_to_csv():
    test_csv_file = os.path.join(os.path.dirname(__file__), 'cats.zip')
    out = list(nycdb.transform.to_csv(nycdb.transform.extract_csvs_from_zip(test_csv_file)))
    assert len(out) == 4
    assert out[0] == {'name': 'alice', 'superpower': 'eating'}
    assert out[1] == {'name': 'fluffy', 'superpower': 'purring'}
    assert out[2] == {'name': 'meowses', 'superpower': 'sitting'}


def test_to_bbl_with_borough_field():
    table = [{'borough': 'queens', 'block': '1', 'lot': '1'}, {'borough': 'queens', 'block': '1', 'lot': '2'}]
    out = list(nycdb.transform.with_bbl(table))
    assert out[0] == {'borough': 'queens', 'block': '1', 'lot': '1', 'bbl': '4000010001'}
    assert out[1] == {'borough': 'queens', 'block': '1', 'lot': '2', 'bbl': '4000010002'}


def test_to_bbl_with_boro_field():
    table = [{'boro': 'queens', 'block': '1', 'lot': '1'}, {'boro': 'queens', 'block': '1', 'lot': '2'}]
    out = list(nycdb.transform.with_bbl(table, borough='boro'))
    assert out[0] == {'boro': 'queens', 'block': '1', 'lot': '1', 'bbl': '4000010001'}
    assert out[1] == {'boro': 'queens', 'block': '1', 'lot': '2', 'bbl': '4000010002'}


def test_flip_numbers_nothing_to_flip():
    # assert nycdb.transform.flip_numbers(['one1', 'two2']) == ['one1', 'two2']
    assert nycdb.transform.flip_numbers('one1') == 'one1'
    assert nycdb.transform.flip_numbers('one1234') == 'one1234'
    assert nycdb.transform.flip_numbers('one1234two') == 'one1234two'


def test_flip_numbers():
    assert nycdb.transform.flip_numbers('1one') == 'one1'
    assert nycdb.transform.flip_numbers('123one') == 'one123'


def test_iso_dates_to_text():
    table = [{'a': '2023-01-04T00:00:00.000', 'b': '2019-04-17T00:00:00.000'},
             {'a': '01/04/2023', 'b': None}]
    out = list(nycdb.transform.iso_dates_to_text(nycdb.transform.iso_dates_to_text(table, ['a']), ['b'], '%m/%Y'))
    assert out == [{'a': '01/04/2023', 'b': '04/2019'}, {'a': '01/04/2023', 'b': None}]


def test_skip_fields():
    table = [{'a': 1, 'b': 2, 'c': 3}, {'a': 'x', 'b': 'y', 'c': 'y'}]
    fields_to_skip = frozenset(['c'])
    out = list(nycdb.transform.skip_fields(table, fields_to_skip))
    assert out == [{'a': 1, 'b': 2}, {'a': 'x', 'b': 'y'}]
