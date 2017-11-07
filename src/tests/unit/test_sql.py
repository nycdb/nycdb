import nycdb 
from collections import OrderedDict

def test_create_table():
    fields = OrderedDict([('address', 'text'), ('block', 'integer')])
    assert nycdb.sql.create_table('hello', fields) == 'CREATE TABLE hello (address text, block integer)'
