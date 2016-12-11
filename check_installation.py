"""
USE: python3 check_installation.py "db_connection_string"

or if you set the environment variable: "NYCDB_CONNECTION_STRING",
you can run the program just as: python3 check_installation.py

"""
import sys
import os
import psycopg2


if len(sys.argv) == 2:
    db_connection_string = sys.argv[1]
elif 'NYCDB_CONNECTION_STRING' in os.environ:
    db_connection_string = os.environ['NYCDB_CONNECTION_STRING']
else:
    raise Exception("You must pass the db connection string as the first argument to the script or set the environment variable: NYCDB_CONNECTION_STRING")


def table_exists(cur, table_name):    
    query = "SELECT EXISTS(SELECT 1 FROM information_schema.tables where table_name = '{0}')".format(table_name)
    cur.execute(query)
    return cur.fetchone()[0]

def schema_helper(table_name):
    if table_name in ['contacts', 'corporate_owners', 'registrations', 'registrations_grouped_by_bbl']:
        return "hpd.{}".format(table_name)
    else:
        return table_name
    
def row_count(cur, table_name):
    query = "SELECT COUNT(*) from {0}".format(schema_helper(table_name))
    cur.execute(query)
    return cur.fetchone()[0]
    

conn = psycopg2.connect(db_connection_string)
cursor = conn.cursor()

tables = [ 'pluto_16v2', 'dobjobs', 'violations', 'uniq_violations', 'open_violations', 'all_violations', 'contacts', 'corporate_owners', 'registrations', 'registrations_grouped_by_bbl', 'dof_sales', 'rentstab' ]
for table in tables:
    if table_exists(cursor, table):
        print(table + ' has ' + str(row_count(cursor, table)) + ' rows')
    else:
        print(table + ' is missing!')

conn.close()    
