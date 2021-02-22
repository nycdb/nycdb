from nycdb.address import normalize_street, normalize_street_number, normalize_apartment

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
        assert normalize_street('VAN CORTLANDT PK SO') == 'VAN CORTLANDT PARK SOUTH'

    def test_place_lane(self):
        assert normalize_street('313 PL N.') == '313TH PLACE NORTH'
        assert normalize_street('302 LN') == '302ND LANE'

    def test_street(self):
        assert normalize_street('102nd ST') == '102ND STREET'
        assert normalize_street('E 102nd ST') == 'EAST 102ND STREET'
        assert normalize_street('E 102nd ST') == 'EAST 102ND STREET'
        assert normalize_street('W 3rd ST.') == 'WEST THIRD STREET'
        assert normalize_street('S 3rd ST') == 'SOUTH THIRD STREET'
        assert normalize_street('North 10 ST') == 'NORTH TENTH STREET'

        assert normalize_street('RIVERSIDE DRIVE') == 'RIVERSIDE DRIVE'
        assert normalize_street('RIVERSIDE DR E') == 'RIVERSIDE DRIVE EAST'
        assert normalize_street('CAMPBELL DR.') == 'CAMPBELL DRIVE'
        assert normalize_street('SOME TERRACE') == 'SOME TERRACE'
        assert normalize_street('SOME PLAZA') == 'SOME PLAZA'
        assert normalize_street('SOME ST STATION') == 'SOME STREET STATION'

    def test_ave(self):
        assert normalize_street('AVENUE W') == 'AVENUE W'

    def test_blvd_parkway(self):
        assert normalize_street('queens BLVD') == 'QUEENS BOULEVARD'
        assert normalize_street('OCEAN PKWY N') == 'OCEAN PARKWAY NORTH'

    def test_saints(self):
        assert normalize_street('ST. MARKS') == 'SAINT MARKS'
        assert normalize_street('W. ST JAMES ST.') == 'WEST SAINT JAMES STREET'

    def test_aliases(self):
        result = 'ADAM CLAYTON POWELL JR BOULEVARD'
        assert normalize_street('ADAM CLAYTON POWELL') == result
        assert normalize_street('ADAM CLAYTON POWELL JR') == result
        assert normalize_street('ADAM CLAYTON POWELL JR BLVD') == result
        assert normalize_street('AVENUE OF AMERICAS') == 'AVENUE OF THE AMERICAS'
        assert normalize_street('COLLEGE PT BLVD') == 'COLLEGE POINT BOULEVARD'
        assert normalize_street('COLLEGE PT. BLVD') == 'COLLEGE POINT BOULEVARD'
        assert normalize_street('CO-OP CITY') == 'COOP CITY'


def test_normalize_street_number():
    assert normalize_street_number(None) is None
    assert normalize_street_number('') is None
    assert normalize_street_number('24') == '24'
    assert normalize_street_number('101-23') == '101-23'
    assert normalize_street_number('30 80') == '30 80'
    assert normalize_street_number(' 301  ') == '301'


def test_normalize_apartment_returns_nil():
    assert normalize_apartment(None) is None
    assert normalize_apartment('') is None
    assert normalize_apartment('    ') is None
    assert normalize_apartment('-') is None


def test_normalize_apartment_simple():
    assert normalize_apartment('123') == '123'
    assert normalize_apartment('28X') == '28X'
    assert normalize_apartment('28-X') == '28X'
    assert normalize_apartment('28 x') == '28X'
    assert normalize_apartment('28_x') == '28X'
    assert normalize_apartment('#17G') == '17G'


def test_normalize_apartment_floor():
    assert normalize_apartment('2FW') == "2FLOOR"
    assert normalize_apartment('12FL') == "12FLOOR"
    assert normalize_apartment('12 FL') == "12FLOOR"
    assert normalize_apartment('12-FL') == "12FLOOR"
    assert normalize_apartment('12-FLOOR') == "12FLOOR"
    assert normalize_apartment('12 FLOOR') == "12FLOOR"
    assert normalize_apartment('12TH FLOOR') == "12FLOOR"
    assert normalize_apartment('12 FL.') == "12FLOOR"
    assert normalize_apartment('12THFL') == "12FLOOR"
    assert normalize_apartment('12 FLO') == "12FLOOR"
    assert normalize_apartment('12 FLO.') == "12FLOOR"
    assert normalize_apartment('12 FLR') == "12FLOOR"

    assert normalize_apartment('3RD FL.') == "3FLOOR"
    assert normalize_apartment('3RDFL') == "3FLOOR"

    assert normalize_apartment('10F') == '10F'
    assert normalize_apartment('10TH F') == '10FLOOR'
