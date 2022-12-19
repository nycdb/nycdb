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
    assert typecast.integer(None) is None
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
    assert typecast.char(None, 3) is None


def test_boolean():
    assert typecast.boolean('TRUE') is True
    assert typecast.boolean('x') is True
    assert typecast.boolean('X') is True
    assert typecast.boolean('no') is False
    assert typecast.boolean('am i true or false?') is None
    assert typecast.boolean(None) is None


def test_numeric():
    assert typecast.numeric('1.5') == Decimal('1.5')
    assert typecast.numeric('') is None
    assert typecast.numeric(None) is None


def test_to_float():
    assert typecast.to_float(12.5) == 12.5
    assert typecast.to_float('12.5') == 12.5
    assert typecast.to_float('not a number') is None
    assert typecast.to_float(None) is None


def test_date_yyyymmdd_string():
    assert typecast.date('19250501') == datetime.date(1925, 5, 1)


def test_date_invalid_yyyymmdd_string():
    assert typecast.date('19940231') is None


def test_date_mm_dd_yyyy():
    assert typecast.date('05/01/1925') == datetime.date(1925, 5, 1)
    assert typecast.date('5/1/1925') == datetime.date(1925, 5, 1)
    assert typecast.date('5/1/22') == datetime.date(2022, 5, 1)
    assert typecast.date('5/1/95') == datetime.date(1995, 5, 1)


def test_date_iso8601_string():
    assert typecast.date('1925-05-01') == datetime.date(1925, 5, 1)
    assert typecast.date('1925-5-1') == datetime.date(1925, 5, 1)


def test_date_invalid_iso8601_string():
    assert typecast.date('1994-02-31') is None


def test_date_accepts_datetime():
    assert typecast.date(datetime.date(1925, 5, 1)) == datetime.date(1925, 5, 1)


def test_date_bad_str():
    assert typecast.date('03/04/2015 12:00:00 AM XYZ') is None
    assert typecast.date('01/01/0000') is None
    assert typecast.date('WHATHAPP') is None

def test_date_none():
    assert typecast.date(None) is None


def test_date_mm_dd_yyyy_with_timestamp():
    assert typecast.date('03/04/2015 12:00:00 AM') == datetime.date(2015, 3, 4)


def test_time():
    assert typecast.time('15:01:00') == datetime.time(hour=15, minute=1, second=0)
    assert typecast.time('15:1:0') == datetime.time(hour=15, minute=1, second=0)
    assert typecast.time('3:01:00 PM') == datetime.time(hour=15, minute=1, second=0)
    assert typecast.time('3:01:00 AM') == datetime.time(hour=3, minute=1, second=0)
    assert typecast.time(datetime.time.min) == datetime.time.min
    assert typecast.time('RIGHT NOW') is None
    assert typecast.time(None) is None


def test_timestamp():
    assert typecast.timestamp('2020-05-13 23:30:00') == datetime.datetime(2020, 5, 13, 23, 30, 0)
    assert typecast.timestamp('05/13/2020 23:30:00') == datetime.datetime(2020, 5, 13, 23, 30, 0)
    assert typecast.timestamp('2020-05-13 11:30:00 PM') == datetime.datetime(2020, 5, 13, 23, 30, 0)
    assert typecast.timestamp('2020-05-13 11:30:00 AM') == datetime.datetime(2020, 5, 13, 11, 30, 0)
    assert typecast.timestamp(datetime.datetime(2020, 5, 13, 11, 30, 0)) == datetime.datetime(2020, 5, 13, 11, 30, 0)


def test_timestamp_bad_str():
    assert typecast.timestamp('2020-02-31 23:30:00') == None
    assert typecast.timestamp('05/13/2020 23:30:00 AM XYZ') == None
    assert typecast.timestamp('WHATHAPP') == None

def test_timestamp_none():
    assert typecast.timestamp(None) is None

def test_text_array():
    assert typecast.text_array('  one,two,three  ') == ['one', 'two', 'three']
    assert typecast.text_array('1|2|3', sep='|') == ['1', '2', '3']
    assert typecast.text_array(None) is None


def test_typecast_init():
    t = typecast.Typecast(nycdb.datasets()['pluto_16v2']['schema'])

    assert isinstance(t.fields, dict)
    assert t.fields['block'] == 'integer'
    assert isinstance(t.cast, dict)


def test_typecast_generate_cast():
    t = typecast.Typecast(nycdb.datasets()['hpd_complaints']['schema'][0])
    assert t.cast['boroughid']('123') == 123
    assert t.cast['borough'](' test  ') == 'test'
    assert t.cast['bbl']('0123456789X') == '0123456789'


def test_cast_row():
    t = typecast.Typecast(nycdb.datasets()['hpd_complaints']['schema'][0])
    row = { 'BoroughID': '123', 'Status': 'GOOD' }
    assert t.cast_row(row) == { 'BoroughID': 123, 'Status': 'GOOD' }


def test_correct_bbl_typecast_for_pluto():
    t = typecast.Typecast(nycdb.datasets()['pluto_16v2']['schema'])
    assert t.cast['bbl']('1008300028') == '1008300028'
    assert t.cast['bbl']('1008300028.00') == '1008300028'
    
