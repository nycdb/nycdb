import csv
import io
import types
import pyproj
from zipfile import ZipFile
from pyproj import *

from .bbl import bbl
from .utility import merge

invalid_header_chars = [ "\n", "\r", ' ', '-', '#', '.', "'", '"', '_' ]

def clean_headers(headers):
    s = headers.lower()
    for char in invalid_header_chars:
        s = s.replace(char, '')
    return s.split(',')


# String (filepath) -> String
def extract_csvs_from_zip(file_path):
    """
    Combines all content in all CSVs (.csv) in the zip file.

    Uses the header from the first csv file and 
    excludes the header from the rest of the csvs.
    
    Returns generator
    """
    with ZipFile(file_path, 'r') as zip_f:
        csv_files = [ f for f in zip_f.namelist() if f[-3:].lower() == 'csv' ]
        for (idx, csv) in enumerate(csv_files):
            with zip_f.open(csv) as f:
                firstline = f.readline().decode('UTF-8', 'ignore')
                if idx == 0:
                    yield firstline
                for line in f:
                    yield line.decode('UTF-8', 'ignore')


def to_csv(file_path_or_generator):
    """ 
    input: String | Generator
    outs: Generator

    reads firstline as the headers and converts input into a stream of dicts
    """
    if isinstance(file_path_or_generator, types.GeneratorType):
        f = io.StringIO(''.join(list(file_path_or_generator)))
    elif isinstance(file_path_or_generator, str):
        f = open(file_path_or_generator, 'r')
    else:
        raise ValueError("to_csv accepts Strings or Generators")

    with f:
        headers = clean_headers(f.readline())
        for row in csv.DictReader(f, fieldnames=headers):
            yield row


def with_bbl(table):
    for row in table:
        yield merge(row, {'bbl': bbl(row['borough'], row['block'], row['lot'])})


p4j = '+proj=lcc +lat_1=40.66666666666666 +lat_2=41.03333333333333 +lat_0=40.16666666666666 +lon_0=-74 +x_0=300000 +y_0=0 +datum=NAD83 +units=us-ft +no_defs '
ny_state_plane = pyproj.Proj(p4j, preserve_units=True)
wgs84 = pyproj.Proj(init="epsg:4326")

def ny_state_coords_to_lat_lng(xcoord, ycoord):
    return pyproj.transform(ny_state_plane, wgs84, xcoord, ycoord)


def with_geo(table):
    for row in table:
        try:
            coords = ( float(row['xcoord']), float(row['ycoord']) )
            lng, lat = ny_state_coords_to_lat_lng(*coords)
            yield merge(row, { 'lng': lng, 'lat': lat })
        except:
            yield merge(row, { 'lng': None, 'lat': None })
