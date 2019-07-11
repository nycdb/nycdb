import csv
import io
import re
import types
from zipfile import ZipFile

from .address import normalize_street, normalize_street_number, normalize_apartment
from .bbl import bbl
from .utility import merge
from .geo import ny_state_coords_to_lat_lng

invalid_header_chars = ["\n", "\r", ' ', '-', '#', '.', "'", '"', '_', '/', '(', ')', ':']
replace_header_chars = [('%', 'pct')]
starts_with_numbers = re.compile(r'^(\d+)(.*)$')
only_numbers = re.compile(r'^\d+$')


def flip_numbers(header):
    """
    str -> str
    If the header starts with numbers, it places
    those numbers at the end of the string.

    Columns in SQL cannot start with a number. This function will change
    a header named '2017values' to 'values2017'
    """
    match = starts_with_numbers.match(header)
    if match:
        if only_numbers.match(header):
            raise "Column names cannot be composed of all numbers"
        else:
            return (match.group(2) + match.group(1))
    else:
        return header


def clean_headers(headers):
    """
    str -> [str]
    turns header line into a list and fixes some commmon

    issues with column names
    """
    s = headers.lower()
    for char in invalid_header_chars:
        s = s.replace(char, '')
    for old, new in replace_header_chars:
        s = s.replace(old, new)
    return [flip_numbers(x) for x in s.split(',')]


# String (filepath) -> String
def extract_csvs_from_zip(file_path):
    """
    Combines all content in all CSVs (.csv) in the zip file.

    Uses the header from the first csv file and
    excludes the header from the rest of the csvs.

    Returns generator
    """
    with ZipFile(file_path, 'r') as zip_f:
        csv_files = [f for f in zip_f.namelist() if f[-3:].lower() == 'csv']
        for (idx, csv_file) in enumerate(csv_files):
            with zip_f.open(csv_file) as f:
                firstline = f.readline().decode('UTF-8', 'ignore')
                if idx == 0:
                    yield firstline
                for line in f:
                    yield line.decode('UTF-8', 'ignore')


def extract_csv_from_zip(file_path, csv_file_path):
    """
    Returns a generator that iterates through all the rows
    in the given CSV file in the given ZIP file, including
    the header row.
    """

    with ZipFile(file_path, 'r') as zip_f:
        with zip_f.open(csv_file_path) as f:
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
        f = open(file_path_or_generator, mode='r', encoding='utf-8', errors='replace')
    else:
        raise ValueError("to_csv accepts Strings or Generators")

    with f:
        headers = clean_headers(f.readline())
        for row in csv.DictReader(f, fieldnames=headers):
            yield row


def with_bbl(table, borough='borough', block='block', lot='lot'):
    for row in table:
        yield merge(row, {'bbl': bbl(row[borough], row[block], row[lot])})


def with_geo(table):
    for row in table:
        try:
            coords = (float(row['xcoord']), float(row['ycoord']))
            lng, lat = ny_state_coords_to_lat_lng(*coords)
            yield merge(row, {'lng': lng, 'lat': lat})
        except:
            yield merge(row, {'lng': None, 'lat': None})


def skip_fields(table, fields_to_skip):
    for row in table:
        for f in fields_to_skip:
            if f in row:
                del row[f]
        yield row


##
# standardize addresses in hpd contact and registration:
#

def hpd_registrations_address_cleanup(rows):
    for row in rows:
        row['housenumber'] = normalize_street_number(row['housenumber'])
        row['streetname'] = normalize_street(row['streetname'])
        yield row


def hpd_contacts_address_cleanup(rows):
    for row in rows:
        row['businesshousenumber'] = normalize_street_number(row['businesshousenumber'])
        row['businessstreetname'] = normalize_street(row['businessstreetname'])
        row['businessapartment'] = normalize_apartment(row['businessapartment'])
        yield row
