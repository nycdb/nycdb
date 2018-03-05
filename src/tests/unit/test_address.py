from nycdb.address import normalize_street

# def test_simple_address():
# #     assert nycdb.address.normalize('123 Main Street') == '123 Main Street'

# 3ND
# 3RD
# 4TH
# 5TH
# 6TH
# 7TH
# 8TH
# 9TH
# 10TH



class TestNormalizeStreet(object):

    def test_numbers(self):
        assert normalize_street('2nd AVENUE') == 'SECOND AVENUE'
        assert normalize_street('2 ave') == 'SECOND AVENUE'
        assert normalize_street('SECOND ave') == 'SECOND AVENUE'
        assert normalize_street('FIRST ave') == 'FIRST AVENUE'
        assert normalize_street('1ST E. AVE') == 'FIRST EAST AVENUE'

    def test_street(self):
        assert normalize_street('102nd ST') == '102ND STREET'
        assert normalize_street('E 102nd ST') == 'EAST 102ND STREET'
        assert normalize_street('E 102nd ST') == 'EAST 102ND STREET'
        assert normalize_street('W 3rd ST.') == 'WEST THIRD STREET'
        assert normalize_street('North 10 ST') == 'NORTH TENTH STREET'

    def test_blvd(self):
        assert normalize_street('queens BLVD') == 'QUEENS BOULEVARD'
