from .transform import *
from .typecast import Typecast

def pluto_16v2(dataset):
    return with_geo(to_csv(extract_csvs_from_zip(dataset.files[0].dest)))
    

def hpd_complaints(dataset):
    return with_bbl(to_csv(dataset.files[0].dest))


def dob_complaints(dataset):
    return to_csv(dataset.files[0].dest)

def hpd_violations(dataset):
    return to_csv(dataset.files[0].dest)

def hpd_registrations(dataset):
    return to_csv(dataset.files[0].dest)

def hpd_contacts(dataset):
    return to_csv(dataset.files[1].dest)

def dof_sales(dataset):
    xls_files = [ f.dest for f in datasets.files ]
    
