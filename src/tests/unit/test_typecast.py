import nycdb
import datetime
from nycdb import typecast
from unittest.mock import patch
from types import SimpleNamespace
from decimal import Decimal

ARGS = SimpleNamespace(user='postgres', password='password', host='127.0.0.1', database='postgres', port='7777', root_dir='./data')

def test_integer():
    assert typecast.integer(10) == 10
    assert typecast.integer('10') == 10
    assert typecast.integer('  10  ') == 10
    assert typecast.integer('') is None
    assert typecast.integer('NOT AN INTEGER') is None

def test_integer_with_decimal():
    assert typecast.integer('.') is None
    assert typecast.integer('1.0') == 1
    assert typecast.integer('25.923432') == 25

def test_integer_money_str():
    assert typecast.integer('$125') == 125
    assert typecast.integer('$125.00') == 125
    assert typecast.integer('$125.75') == 125

def test_char():
    assert typecast.char('test', 10) == 'test'
    assert typecast.char('test', 2) == 'te'
    assert typecast.char(' test', 2) == 'te'
    assert typecast.char(345, 3) == '345'

def test_boolean():
    assert typecast.boolean('TRUE') is True
    assert typecast.boolean('no') is False
    assert typecast.boolean('am i true or false?') is None

def test_numeric():
    assert typecast.numeric('1.5') == Decimal('1.5')
    assert typecast.numeric('') is None

def test_date_mm_dd_yyyy():
    assert typecast.date('05/01/1925') == datetime.date(1925, 5, 1)

def test_date_accepts_datetime():
    assert typecast.date(datetime.date(1925, 5, 1)) == datetime.date(1925, 5, 1)

def test_date_bad_str():
    assert typecast.date('01/01/01') is None
    assert typecast.date('03/04/2015 12:00:00 AM XYZ') is None
    assert typecast.date('01/01/0000') is None

def test_date_mm_dd_yyyy_with_timestamp():
    assert typecast.date('03/04/2015 12:00:00 AM') == datetime.date(2015, 3, 4)
    
def test_text_array():
    assert typecast.text_array('  one,two,three  ') == ['one', 'two', 'three']
    assert typecast.text_array('1|2|3', sep='|') == ['1', '2', '3']

def test_typecast_init():
    t = typecast.Typecast(nycdb.datasets()['pluto_16v2']['schema'])
    
    assert isinstance(t.fields, dict)
    assert t.fields['block'] == 'integer'
    assert isinstance(t.cast, dict)


def test_typecast_generate_cast():
    t = typecast.Typecast(nycdb.datasets()['hpd_complaints']['schema'])
    assert t.cast['boroughid']('123') == 123
    assert t.cast['borough'](' test  ') == 'test'
    assert t.cast['bbl']('0123456789X') == '0123456789'


def test_cast_row():
    t = typecast.Typecast(nycdb.datasets()['hpd_complaints']['schema'])
    row = { 'BoroughID': '123', 'Status': 'GOOD' }
    assert t.cast_row(row) == { 'BoroughID': 123, 'Status': 'GOOD' }


def test_correct_bbl_typecast_for_pluto():
    t = typecast.Typecast(nycdb.datasets()['pluto_16v2']['schema'])
    assert t.cast['bbl']('1008300028') == '1008300028'
    assert t.cast['bbl']('1008300028.00') == '1008300028'
    
