""" create BBL  """
import re

manhattan_values = [ 'manhattan', 'mn', '1', 1 ]
bronx_values = [ 'bronx', 'the bronx', 'bx', '2', 2 ]
brooklyn_values = [ 'brooklyn', 'bklyn', 'bk' , '3', 3 ]
queens_values = [ 'queens', 'qn', '4', 4 ]
staten_island_values = [ 'staten island', 'si', '5', 5 ]


def boro_to_code(boro):
    if isinstance(boro, str):
        b = boro.strip().lower()
    else:
        b = boro

    if b in manhattan_values:
        code = '1'
    elif b in bronx_values:
        code = '2'
    elif b in brooklyn_values:
        code = '3'
    elif b in queens_values:
        code = '4'
    elif b in staten_island_values:
        code = '5'
    else:
        # print('Incorrect borough: ' + boro)
        code = '0'
    return code


def lot_length_helper(lot):
    if len(lot) == 5:
        return  lot[1:]
    elif len(lot) < 5:
        return lot.zfill(4)
    else:
        # print(lot + " is more than 5 chars long!")
        return '0000'

def is_empty(i):
    """
    Determines if i is empty
    """
    if isinstance(i, int):
        return False

    if isinstance(i, str) and re.match(r'^\d+$', i.strip()):
        return False

    return True


def bbl(boro, block, lot):
    if boro is None or is_empty(block) or is_empty(lot):
        return None

    return boro_to_code(boro) + str(block).zfill(5) + lot_length_helper(str(lot))
