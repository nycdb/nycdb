import nycdb

def test_ny_state_coords_to_lat_lng():
    coords = [987838, 195989]
    result = nycdb.geo.ny_state_coords_to_lat_lng(*coords)
    expected = [-73.98706, 40.70462]
    assert list(map(lambda x: round(x, 5), result)) == expected
