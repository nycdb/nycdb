from .transform import *
from .typecast import Typecast

def pluto_16v2(dataset):
    lines = extract_csvs_from_zip(dataset.files[0].dest).split('\n')
    header = lines[0]
    

def hpd_complaints(dataset):
    return with_bbl(to_csv(dataset.files[0].dest))


def dob_complaints(dataset):
    return to_csv(dataset.files[0].dest)
