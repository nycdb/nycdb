import csv
import io
import types
from zipfile import ZipFile
from .bbl import bbl
        
        
def merge(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z


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
        headers = f.readline().lower().replace("\n", '').replace(' ', '_').split(',')
        for row in csv.DictReader(f, fieldnames=headers):
            yield row


def with_bbl(table):
    for row in table:
        yield merge(row, {'bbl': bbl(row['borough'], row['block'], row['lot'])})
