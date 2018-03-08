from nycdb.address import normalize_street

class TestNormalizeStreet(object):

    def test_simple_address(self):
        assert normalize_street('123 Main Street') == '123RD MAIN STREET'

    def test_broadway(self):
        assert normalize_street('bdwy') == 'BROADWAY'
        assert normalize_street('W BROAD WAY') == 'WEST BROADWAY'

    def test_numbers(self):
        assert normalize_street('2nd AVENUE') == 'SECOND AVENUE'
        assert normalize_street('2nd AVENUE.') == 'SECOND AVENUE'
        assert normalize_street('2 ave') == 'SECOND AVENUE'
        assert normalize_street('SECOND ave') == 'SECOND AVENUE'
        assert normalize_street('FIRST ave') == 'FIRST AVENUE'
        assert normalize_street('1ST E. AVE') == 'FIRST EAST AVENUE'

    def test_remove(self):
        assert normalize_street('78TH ST - BENSONHURST') == '78TH STREET'

    def test_part(self):
        assert normalize_street('VAN CORTLANDT PK SO') == 'VAN CORTLANDT PK SOUTH'

    def test_place_lane(self):
        assert normalize_street('313 PL N.') == '313TH PLACE NORTH'
        assert normalize_street('302 LN') == '302ND LANE'
        
    def test_street(self):
        assert normalize_street('102nd ST') == '102ND STREET'
        assert normalize_street('E 102nd ST') == 'EAST 102ND STREET'
        assert normalize_street('E 102nd ST') == 'EAST 102ND STREET'
        assert normalize_street('W 3rd ST.') == 'WEST THIRD STREET'
        assert normalize_street('North 10 ST') == 'NORTH TENTH STREET'

    def test_blvd(self):
        assert normalize_street('queens BLVD') == 'QUEENS BOULEVARD'


    def test_saints(self):
        assert normalize_street('ST. MARKS') == 'SAINT MARKS'
        assert normalize_street('W. ST JAMES ST.') == 'WEST SAINT JAMES STREET'
        
