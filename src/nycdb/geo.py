import pyproj

ny_state_plane = pyproj.Proj("epsg:2263", preserve_units=True)
wgs84 = pyproj.Proj(init="epsg:4326")
transformer = pyproj.Transformer.from_proj(ny_state_plane, wgs84)

def ny_state_coords_to_lat_lng(xcoord, ycoord):
    return transformer.transform(xcoord, ycoord)
