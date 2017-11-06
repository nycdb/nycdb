YES_VALUES = [ 1, True, 'T', 't', 'true', 'True', 'TRUE', '1', 'y', 'Y', "YES", 'Yes']
NO_VALUES = [ '0', 0, False, 'False', 'f', 'F', 'false', 'FALSE', 'N', 'n', 'NO', 'No', 'no']

def integer(i):
    if isinstance(i, int):
        return i
    else:
        return int(i.strip())

def text(x):
    return x

def char(x, n):
    if len(x) > n:
        return x.strip()[0:n]
    else:
        return x

def boolean(x):
    if x in YES_VALUES:
        return True
    elif x in NO_VALUES:
        return False
    else:
        return None
    

class Typecast():
    def __init__(self, dataset):
        pass

    def row(self, row):
        pass
