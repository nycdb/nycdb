from nycdb import typecast

def test_integer():
    assert typecast.integer(10) == 10
    assert typecast.integer('10') == 10
    assert typecast.integer('  10  ') == 10

def test_char():
    assert typecast.char('test', 10) == 'test'
    assert typecast.char('test', 2) == 'te'
    assert typecast.char(' test', 2) == 'te'

def test_boolean():
    assert typecast.boolean('TRUE') is True
    assert typecast.boolean('no') is False
    assert typecast.boolean('am i true or false?') is None

