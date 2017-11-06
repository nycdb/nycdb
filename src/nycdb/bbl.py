""" create BBL  """

def boro_to_code(boro):
    b = boro.strip()
    if b == 'MANHATTAN':
        code = '1'
    elif b == 'BRONX':
        code = '2'
    elif b == 'BROOKLYN':
        code = '3'
    elif b == 'QUEENS':
        code = '4'
    elif b == 'STATEN ISLAND':
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

def bbl(boro, block, lot):
    if boro is None or block is None or lot is None:
        return None
    else:
        return boro_to_code(boro.upper()) + str(block).zfill(5) + lot_length_helper(str(lot))
