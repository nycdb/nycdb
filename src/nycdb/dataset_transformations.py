from .transfrom import *

def pluto_16v2(dataset):
    lines = extract_csvs_from_zip(dataset.files[0].dest).split('\n')
    header = lines[0]
    

    



