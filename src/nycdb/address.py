"""
Functions to standardize address strings
in HPD contacts data
"""
import re
# import functools


STREETS = [
    ( ('AVENUE', 'AVE'), 'AVENUE' ),
    ( (' STREET', ' STR', ' ST\.?'), ' STREET' ),
    ( ('PLACE', 'PL'), 'PLACE' ),
    ( ('ROAD', '(?<!\d)RD'), 'ROAD'),
    ( ('LANE', 'LN'), 'LANE' ),
    ( ('BOULEVARD', 'BLVD'), 'BOULEVARD')
]

# 123 E. SECOND AVE

# These have spaces at the end to avoid
# replace letters in the middle of words
# and named aveneues such as "Avenue W"
DIRECTIONS = [
    ( ('EAST ', '(^E\.? )'), 'EAST ' ),
    ( ('WEST ', '(^W\.? )'), 'WEST ' ),
    ( ('NORTH ', '(^N\.? )'), 'NORTH ' ),
    ( ('SOUTH ', '(^S\.? )'), 'SOUTH ' ),
    ( (' EAST ', '((?<!AVENUE)( E\.? ))'), ' EAST ' ),
    ( (' WEST ', '((?<!AVENUE)( W\.? ))'), ' WEST ' ),
    ( (' NORTH ', '((?<!AVENUE)( N\.? ))'), ' NORTH ' ),
    ( (' SOUTH ', '((?<!AVENUE)( S\.? ))'), ' SOUTH ' )
]


NUMBERS = [
    ( ('^1(ST)? ', ), 'FIRST '),
    ( ('^2(ND)? ', ), 'SECOND '),
    ( ('^3(RD)? ', ), 'THIRD '),
    ( ('^4(TH)? ', ), 'FOURTH '),
    ( ('^5(TH)? ', ), 'FIFTH '),
    ( ('^6(TH)? ', ), 'SIXTH '),
    ( ('^7(TH)? ', ), 'SEVENTH '),
    ( ('^8(TH)? ', ), 'EIGHTH '),
    ( ('^9(TH)? ', ), 'NINTH '),
    ( ('^10(TH)? ', ), 'TENTH '),
    ( (' 1(ST)? ',), ' FIRST '),
    ( (' 2(ND)? ',), ' SECOND '),
    ( (' 3(RD)? ',), ' THIRD '),
    ( (' 4(TH)? ',), ' FOURTH '),
    ( (' 5(TH)? ',), ' FIFTH '),
    ( (' 6(TH)? ',), ' SIXTH '),
    ( (' 7(TH)? ',), ' SEVENTH '),
    ( (' 8(TH)? ',), ' EIGHTH '),
    ( (' 9(TH)? ',), ' NINTH '),
    ( (' 10(TH)? ',), ' TENTH ')
]


REGEX_REPLACEMENTS = STREETS + DIRECTIONS + NUMBERS

# Iter, Str -> Lambda
def replace_func(patterns, replacement):
    pattern = ('|').join(patterns)
    return lambda s: re.sub(pattern, replacement, s)

REGEX_FUNCS = list(map(lambda x: replace_func(x[0], x[1]), REGEX_REPLACEMENTS))


def saints(s):
    re.search("(ST.|SAINT)(\w+)()")


# list(of functions), str -> str
def func_chain(funcs, val):
    if len(funcs) == 0:
        return val
    else:
        return func_chain(funcs[1:],funcs[0](val))

def normalize_street(street):
    s = street.strip().upper()
    return func_chain(REGEX_FUNCS, s)

# def normalize_street(street):
#     pass

# def street_name(s):
#     for regex, street in STREET_NAMES:
#         if regex.match(s):
#             return street
#     return s




# def normalize_street(street):
#     out = []
#     split = tuple(map(lambda x: x.strip(), clean(street).split(' ')))
#     # print(split)
#     for x in split:
#         if x in directions:
#             out.append(directions[x])
#         else:
#             street = street_name(x)
#             if street in NORMALIZED_STREETS:
#                 out.append(street)
#             else:
#                 out.append(street)
                

#     return ' '.join(out)
