
"""
USE: python3 check_installation.py --user USER --password PASS --host HOST -- database DATABASE
"""
import argparse
import psycopg2

parser = argparse.ArgumentParser(description='clean and parse department of buildings jobs. Writes cleaned csv to stdout unless option --psql is invoked.')
parser.add_argument("-U", "--user", help="Postgres user. default: postgres", default="postgres")
parser.add_argument("-P", "--password", help="Postgres password. default: postgres", default="postgres")
parser.add_argument("-H", "--host", help="Postgres host: default: 127.0.0.1", default="127.0.0.1")
parser.add_argument("-D", "--database", help="postgres database: default: postgres", default="postgres")
args = parser.parse_args()


class colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def table_exists(cur, table_name):    
    query = "SELECT EXISTS(SELECT 1 FROM information_schema.tables where table_name = '{0}')".format(table_name)
    cur.execute(query)
    return cur.fetchone()[0]

def row_count(cur, table_name):
    query = "SELECT COUNT(*) from {0}".format(table_name)
    cur.execute(query)
    return cur.fetchone()[0]

conn = psycopg2.connect(user=args.user, password=args.password, host=args.host, database=args.database)
cursor = conn.cursor()

tables = ['pluto_16v2', 'dobjobs', 'hpd_violations', 'hpd_uniq_violations', 'hpd_open_violations', 'hpd_all_violations', 'hpd_contacts', 'hpd_corporate_owners', 'hpd_registrations', 'hpd_registrations_grouped_by_bbl', 'dof_sales', 'rentstab', 'complaints_311']

print(colors.BLUE + 'Checking the row count of each table in NYC-DB' + colors.ENDC)

for table in tables:
    if table_exists(cursor, table):
        print(colors.GREEN + table + ' has ' + format(row_count(cursor, table), ',') + ' rows' + colors.ENDC)
    else:
        print(colors.FAIL + table + ' is missing!' + colors.ENDC)

conn.close()    
