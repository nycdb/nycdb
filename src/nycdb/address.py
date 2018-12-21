"""
Functions to standardize address strings
in HPD contacts data
"""
import re

STREETS = [
    (r'(?<= )AVE(NUE)?', 'AVENUE'),
    (r'(?<= )(STREET|STR|(ST\.?))', 'STREET'),
    (r'(?<= )PL(ACE)?', 'PLACE'),
    (r'(?<= )(ROAD|(?<!\d)RD\.?)', 'ROAD'),
    (r'(?<= )(LA(NE)?|LN)', 'LANE'),
    (r'(?<= )CT|CRT', 'COURT'),
    (r'(?<= )DR', 'DRIVE'),
    (r'(?<= )(BOULEVARD|BLVD)', 'BOULEVARD'),
    (r'(?<= )(PKWY|PARKWY)', 'PARKWAY'),
    (r'(?<= )(PK)', 'PARK'),
    (r'(?<= )(BCH)', 'BEACH'),
    (r'(?<= )(TERR)', 'TERRACE'),
    (r'(^|(?<= ))(BDWAY|BDWY|BROAD WAY)', 'BROADWAY')
]


# Look for direction abbrivation as the start of the string or a space, but NOT 'AVENUE '
# this is to avoid lettered avenues such as "AVENUE W"
DIR_START = "(^|(?<=[ ]))(?<!AVENUE )"
DIR_END = "((?=[ ])|$)"

dir_regex = lambda x: DIR_START + x + DIR_END

DIRECTIONS = [
    (dir_regex(r'N\.?'), 'NORTH'),
    (dir_regex(r'SO?\.?'), 'SOUTH'),
    (dir_regex(r'E\.?'), 'EAST'),
    (dir_regex(r'W\.?'), 'WEST')
]

ALIASES = [
    ('ADAM CLAYTON POWELL( JR)?( (BLVD|BOULEVARD))?', 'ADAM CLAYTON POWELL JR BOULEVARD'),
    ('AVENUE OF( THE)? AMERICAS', 'AVENUE OF THE AMERICAS'),
    (r'COLLEGE PT\.? (BLVD|BOULEVARD)', 'COLLEGE POINT BOULEVARD'),
    ('CO-OP CITY', 'COOP CITY')
]

REMOVE = [
    ('(BKLYN|BROOKLYN|QUEENS|BRONX|MANHATTAN|NEW YORK|NYC|SI)$', ''),
    ('(BENSONHURST|CORONA)$', ''),
    (r'\(.+\)$', '')
]

REGEX_REPLACEMENTS = STREETS + DIRECTIONS + REMOVE

# Str, Str -> Lambda
def replace_func(pattern, replacement):
    return lambda s: re.sub(pattern, replacement, s)

ALIASES_FUNCS = list(map(lambda x: replace_func(*x), ALIASES))
REGEX_FUNCS = list(map(lambda x: replace_func(*x), REGEX_REPLACEMENTS))

WORD_NUMBERS = ['ZEROTH', 'FIRST', 'SECOND', 'THIRD',
                'FOURTH', 'FIFTH', 'SIXTH', 'SEVENTH',
                'EIGHTH', 'NINTH', 'TENTH']
SUFFIXES = {
    '0': 'TH',
    '1': 'ST',
    '2': 'ND',
    '3': 'RD',
    '4': 'TH',
    '5': 'TH',
    '6': 'TH',
    '7': 'TH',
    '8': 'TH',
    '9': 'TH'
}


def format_number(matchobj):
    n = matchobj.group('number')
    rest = matchobj.group('rest')
    if int(n) < 11:
        return WORD_NUMBERS[int(n)] + rest
    else:
        tens_digit = str(n)[-2:-1]

        if tens_digit == '1':
            return str(n) + 'TH' + rest
        else:
            return n + SUFFIXES[n[-1]] + rest


def replace_number(string):
    return re.sub(r"(^|(?<=[ ]))(?P<number>\d+)(TH|ST|ND|RD)?(?P<rest>(\b|[ ]).*)", format_number, string)


HOLY_SAINTS = ['JOSEPH', 'MARKS', 'LAWRENCE', 'JAMES',
               'NICHOLAS', 'HOLLIS', 'JOHNS', "JOHN's"]

SAINTS_REGEX = r"ST\.?[ ](?P<street_name>({}))".format('|'.join(HOLY_SAINTS))

def saints(s):
    repl = lambda matchobj: "SAINT " + matchobj.group('street_name')
    return re.sub(SAINTS_REGEX, repl, s)

STREET_FUNCS = ALIASES_FUNCS + [replace_number, saints] + REGEX_FUNCS

# list(of functions), str -> str
def func_chain(funcs, val):
    if len(funcs) == 0:
        return val
    else:
        return func_chain(funcs[1:], funcs[0](val))

def remove_extra_spaces(s):
    return ' '.join([x for x in s.split(' ') if x != ''])


def prepare(s):
    return remove_extra_spaces(s).strip().upper().replace('"', '').replace('-', '')


def normalize_street(street):
    if street is None:
        return None

    s = prepare(street)

    if s == '':
        return None

    return func_chain(STREET_FUNCS, s).replace('.', '').strip()


# remove dashes or spaces...sorry Queens!
def normalize_street_number(number):
    if number is None or number == '':
        return None
    return re.sub(r'(?<=\d)(-|[ ])(?=\d)', '', number).replace('-', '').strip()


APT_STRINGS_TO_REMOVE = ['.', '_', '#', '{', '}', '/']

def clean_apt_str(s):
    s = prepare(s)
    for char_to_remove in APT_STRINGS_TO_REMOVE:
        s = s.replace(char_to_remove, '')
    return s


APT_NUM = r'(?<=\d)(ST|TH|ND|RD)'
# "12F" becomes 12F
# "12TH F" becomes 12FLOOR
EDGE_CASE_FLOOR = APT_NUM + '[ ]F$'
FLOOR_REGEX = r'(?<=\d)[ ]?((FL(OOR|O|R)?)|FW)$'

def normalize_apartment(string):
    if string is None:
        return None

    s = clean_apt_str(string)

    if s == '':
        return None

    s = re.sub(EDGE_CASE_FLOOR, 'FLOOR', s)
    s = re.sub(APT_NUM, '', s)
    s = re.sub(FLOOR_REGEX, 'FLOOR', s)

    return s.replace(' ', '')
