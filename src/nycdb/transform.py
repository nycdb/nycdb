import csv
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
    
    Returns entire contents of all csv as a string (UTF-8)
    """
    content = ''
    with ZipFile(file_path, 'r') as zip_f:
        csv_files = [ f for f in zip_f.namelist() if f[-3:].lower() == 'csv' ]
        for (idx, csv) in enumerate(csv_files):
            with zip_f.open(csv) as f:
                firstline = f.readline().decode('UTF-8', 'ignore')
                if idx == 0:
                    content += firstline  # get header from first line
                content += f.read().decode('UTF-8', 'ignore')
    return content


def to_csv(file_path):
    with open(file_path, 'r') as f:
        headers = f.readline().lower().replace("\n", '').replace(' ', '_').split(',')
        for row in csv.DictReader(f, fieldnames=headers):
            yield row


def with_bbl(table):
    for row in table:
        yield merge(row, {'bbl': bbl(row['borough'], row['block'], row['lot'])})
