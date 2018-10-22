import nycdb

def test_bbl_with_names():
    assert nycdb.bbl.bbl('Bronx', 432, 10) == '2004320010'

def test_string_number():
    assert nycdb.bbl.bbl('1', '100', '50') == '1001000050'

def test_bbl_invalid_lot():
    assert nycdb.bbl.bbl('Brooklyn', 600, 'LOT') is None

def test_bbl_invalid_borough():
    assert nycdb.bbl.bbl('NYC', '600', '1') == '0006000001'
