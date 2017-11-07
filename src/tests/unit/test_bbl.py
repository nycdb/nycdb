import nycdb

def test_bbl_with_names():
    assert nycdb.bbl.bbl('Bronx', 432, 10) == '2004320010'
    
