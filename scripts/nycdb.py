#!/usr/bin/env python3
"""
USE: python3 nycdb.py --user USER --password PASS --host HOST --database DATABASE [--check] [--dump]

Helper program to:
  - check installation
  - dump tables
"""
import argparse
import psycopg2
import datetime
from itertools import chain

def parse_args():
    parser = argparse.ArgumentParser(description='Helper tasks for nycdb')
    parser.add_argument("-U", "--user", help="Postgres user. default: postgres", default="postgres")
    parser.add_argument("-P", "--password", help="Postgres password. default: postgres", default="postgres")
    parser.add_argument("-H", "--host", help="Postgres host: default: 127.0.0.1", default="127.0.0.1")
    parser.add_argument("-D", "--database", help="postgres database: default: postgres", default="postgres")
    parser.add_argument("--check", action="store_true", help="Checks row count of tables in NYCDB")
    parser.add_argument("--dump", action="store_true", help="dumps tables")
    return parser.parse_args()


class colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    
def execute_and_fetchone(cursor, query):
    cursor.execute(query)
    return cursor.fetchone()[0]


def table_exists(cur, table_name):
    query = "SELECT EXISTS(SELECT 1 FROM information_schema.tables where table_name = '{0}')".format(table_name)
    return execute_and_fetchone(cur, query)


def row_count(cur, table_name):
    query = "SELECT COUNT(*) from {0}".format(table_name)
    return execute_and_fetchone(cur, query)


TABLES = {
    'pluto_16v2': [ 'pluto_16v2' ],
    'dobjobs': [ 'dobjobs' ],
    'hpd_violations': [
        'hpd_violations',
        'hpd_uniq_violations',
        'hpd_open_violations',
        'hpd_all_violations'
    ],
    'hpd_registrations': [
        'hpd_contacts',
        'hpd_corporate_owners',
        'hpd_registrations',
        'hpd_registrations_grouped_by_bbl'
    ],
    'dof_sales': ['dof_sales'],
    'rent_stabilization_counts': [ 'rentstab' ],
    '311_complaints': [ 'complaints_311' ],
    'acris': [
        'country_codes',
        'document_control_codes',
        'ucc_collateral_codes',
        'personal_property_legals',
        'personal_property_master',
        'personal_property_parties',
#       'personal_property_references',
#       'personal_property_remarks',
        'real_property_legals',
        'real_property_master',
        'real_property_parties',
        'real_property_references',
        'real_property_remarks'
    ]

}


def check_installation(cursor):
    print(colors.BLUE + 'Checking the row count of each table in NYC-DB' + colors.ENDC)

    all_tables = list(chain.from_iterable(TABLES.values()))

    for table in all_tables:
        if table_exists(cursor, table):
            cnt = row_count(cursor, table)
            if cnt > 0:
                print(colors.GREEN + table + ' has ' + format(cnt, ',') + ' rows' + colors.ENDC)
            else:
                print(colors.FAIL + table + ' has no rows!' + colors.ENDC)
        else:
            print(colors.FAIL + table + ' is missing!' + colors.ENDC)


def dump_table_cmd(table):
    pass

def dump_tables():
    today = datetime.date.today().strftime('%Y_%m_%d')
    for dataset_name, tables in TABLES.items():
        with open("") as out_file:
            for table in tables:
                subprocess.run(dump_table_cmd(table), stdout=out_file)


def main():
    args = parse_args()
    conn = psycopg2.connect(user=args.user, password=args.password, host=args.host, database=args.database)
    cursor = conn.cursor()

    if args.check:
        check_installation(cursor)
    elif args.dump:
        dump_tables()
    else:
        print(colors.BLUE + 'Use --dump to dump tables or --check to check the installation' + colors.ENDC)
        
    conn.close()

if __name__ == '__main__':
    main()
