"""
Typecasting for NYCDB

All values are converted into a suitable python class before
being passed to psycopg2 to be inserted into postgres.
See http://initd.org/psycopg/docs/usage.html#adaptation-of-python-values-to-sql-types
for how psycopg2 converts python types into postgres types
"""

import copy
import re
import datetime
from decimal import Decimal, InvalidOperation

YES_VALUES = [1, True, 'T', 't', 'true', 'True', 'TRUE', '1', 'y', 'Y', "YES", 'Yes', 'x', 'X']
NO_VALUES = ['0', 0, False, 'False', 'f', 'F', 'false', 'FALSE', 'N', 'n', 'NO', 'No', 'no']
INTEGER_TYPES = ['integer', 'smallint', 'bigint', 'int']


def downcase_fields_and_values(d):
    """downcase keys and values in dictionary"""
    return dict((k.lower(), v.strip().lower()) for k, v in d.items())


def integer(i):
    if isinstance(i, int):
        return i
    try:
        int_str = i.strip().replace('$', '')

        if int_str == '.' or int_str == '':
            return None
        elif '.' in i:
            return int(int_str.split('.')[0])
        else:
            return int(int_str)

    except ValueError:
        return None


def text(x):
    if x is None:
        return None
    s = str(x).strip()
    if s == '':
        return None
    else:
        return s


def char(x, n):
    if x is None:
        return None
    val = str(x)
    if len(val) > n:
        return val.strip()[0:n]
    else:
        return val


def numeric(x):
    try:
        return Decimal(x)
    except (InvalidOperation, TypeError):
        return None


def to_float(x):
    if x is None:
        return None
    
    if isinstance(x, float):
        return x

    try:
        return float(x)
    except ValueError:
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
    if isinstance(x, (datetime.date, datetime.datetime)):
        return x
    # checks for 20181231 date input
    if re.match(r'[0-9]{8}', x):
        try:
            return datetime.datetime.strptime(x, '%Y%m%d').date()
        except ValueError:
            return None
    # checks for 12/31/2018 date input
    elif len(x) == 10 and len(x.split('/')) == 3:
        return mm_dd_yyyy(x)
    # checks for 12/31/2018 12:00:00 AM date input
    elif len(x) == 22 and len(x[0:10].split('/')) == 3:
        return mm_dd_yyyy(x)
    else:
        return None


def time(x):
    """
    Converts string into datetime.time
    Example input: 13:01:00
    """
    if isinstance(x, datetime.time):
        return x
    if isinstance(x, str) and re.match(r'^\d{2}:\d{2}:\d{2}$', x.strip()):
        try:
            return datetime.time(*map(int, x.strip().split(':')))
        except ValueError:
            return None


def boolean(x):
    if x in YES_VALUES:
        return True
    elif x in NO_VALUES:
        return False
    else:
        return None


def text_array(x, sep=","):
    return x.strip().split(sep)


def char_cast(n):
    n = copy.copy(n)

    def to_char(x):
        return char(x, n)

    return to_char


class Typecast():
    def __init__(self, schema):
        self.fields = downcase_fields_and_values(schema['fields'])
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
            if 'serial' in v:
                continue
            elif v[0:4] == 'char':
                n = int(re.match(r'char\((\d+)\)', v).group(1))
                d[k] = char_cast(n)
            elif v in INTEGER_TYPES:
                d[k] = lambda x: integer(x)
            elif v == 'text':
                d[k] = lambda x: text(x)
            elif v == 'boolean':
                d[k] = lambda x: boolean(x)
            elif v == 'date':
                d[k] = lambda x: date(x)
            elif 'time' in v:
                d[k] = lambda x: time(x)
            elif v in ['real', 'double precision']:
                d[k] = lambda x: to_float(x)
            elif v == 'numeric':
                d[k] = lambda x: numeric(x)
            elif v == 'text[]':
                d[k] = lambda x: text_array(x)
            else:
                d[k] = lambda x: x
        return d
