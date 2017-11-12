import copy
import re
import datetime
from decimal import Decimal, InvalidOperation

YES_VALUES = [ 1, True, 'T', 't', 'true', 'True', 'TRUE', '1', 'y', 'Y', "YES", 'Yes']
NO_VALUES = [ '0', 0, False, 'False', 'f', 'F', 'false', 'FALSE', 'N', 'n', 'NO', 'No', 'no']
INTEGER_TYPES = [ 'integer', 'smallint', 'bigint', 'int' ]

def downcase_fields_and_values(d):
    """downcase keys and values in dictionary"""
    return dict((k.lower(), v.strip().lower()) for k,v in d.items())

def integer(i):
    if isinstance(i, int):
        return i
    elif '.' in i:
        return int(i.split('.')[0])
    elif i.strip() == '':
        return None
    else:
        return int(i.strip())

def text(x):
    return x.strip()


def char(x, n):
    if len(x) > n:
        return x.strip()[0:n]
    else:
        return x

def numeric(x):
    try:
        return Decimal(x)
    except InvalidOperation:
        return None

def mm_dd_yyyy(date_str):
    try:
        month, day, year = map(int, date_str[0:10].split('/'))
        return datetime.date(year, month, day)
    except ValueError:
        return None

# TODO: allow for different date inputs besides mm/dd/yyyy
#  03/04/2015 12:00:00 AM
def date(x):
    if len(x) == 10 and len(x.split('/')) == 3:
        return mm_dd_yyyy(x)
    elif len(x) == 22 and len(x[0:10].split('/')) == 3:
        return mm_dd_yyyy(x)
    else:
        return None

def boolean(x):
    if x in YES_VALUES:
        return True
    elif x in NO_VALUES:
        return False
    else:
        return None

class Typecast():
    def __init__(self, dataset):
        self.dataset = dataset
        self.fields = downcase_fields_and_values(dataset.dataset['schema']['fields'])
        self.cast = self.generate_cast()


    def cast_rows(self, rows):
        """
        input: Iterable
        output: Iterable
        """
        for row in rows:
            yield self.cast_row(row)
        
    def cast_row(self, row):
        """ 
        Converts values of dictionary by type of dataset
        input: Dict
        output: Dict
        """
        try:
            d = {}
            for column, val in row.items():
                d[column] = self.cast[column.lower()](val)
            return d
        except:
            # print the row for debugging:
            print(row)
            raise
            
    def generate_cast(self):
        """
        Generates conversation table for dataset schema
        """
        d = {}
        for k, v in self.fields.items():
            if v[0:4] == 'char':
                n = int(re.match(r'char\((\d+)\)', v).group(1))
                d[k] = lambda x: char(x, copy.copy(n))
            elif v in INTEGER_TYPES:
                d[k] = lambda x: integer(x)
            elif v == 'text':
                d[k] = lambda x: text(x)
            elif v == 'boolean':
                d[k] = lambda x: boolean(x)
            elif v == 'date':
                d[k] = lambda x: date(x)
            elif v == 'numeric':
                d[k] = lambda x: numeric(x)
            else:
                d[k] = lambda x: x
        return d
