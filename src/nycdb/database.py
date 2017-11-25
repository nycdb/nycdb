import os
import psycopg2
from . import sql

class Database:
    """Database connection to NYCDB"""

    def __init__(self, args, table_name=None):
        self.conn = psycopg2.connect(user=args.user, password=args.password, host=args.host, database=args.database, port=args.port)
        self.table_name = table_name

    def sql(self, SQL):
        """ executes single sql statement """
        with self.conn.cursor() as curs:
            curs.execute(SQL)
        self.conn.commit()

    def insert(self, row):
        """ Inserts one row in a transaction"""
        SQL = sql.insert(self.table_name, row)
        with self.conn.cursor() as curs:
            curs.execute(SQL, row)
        self.conn.commit()
        

    def insert_rows(self, rows):
        """ Inserts many row, all in the same transaction"""
        with self.conn.cursor() as curs:
            for row in rows:
                curs.execute(sql.insert(self.table_name, row), row)
        self.conn.commit()
                
    def execute_sql_file(self, sql_file):
        """ 
        Run the provided sql file.
        Assumes the path is relative to ./sql
        """
        file_path = os.path.join(os.path.dirname(__file__), 'sql', sql_file)
    
        with open(file_path, 'r') as f:
            self.sql(f.read())
