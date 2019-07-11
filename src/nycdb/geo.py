import pyproj

p4j = '+proj=lcc +lat_1=40.66666666666666 +lat_2=41.03333333333333 +lat_0=40.16666666666666 +lon_0=-74 +x_0=300000 +y_0=0 +datum=NAD83 +units=us-ft +no_defs'
ny_state_plane = pyproj.Proj(p4j, preserve_units=True)
wgs84 = pyproj.Proj(init="epsg:4326")
transformer = pyproj.Transformer.from_proj(ny_state_plane, wgs84)

def ny_state_coords_to_lat_lng(xcoord, ycoord):
    return transformer.transform(xcoord, ycoord)


