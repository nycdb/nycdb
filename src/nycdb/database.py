import os
import psycopg2
import psycopg2.extras
from . import sql


class Database:
    """Database connection to NYCDB"""

    def __init__(self, args, table_name=None):
        self.conn = psycopg2.connect(user=args.user, password=args.password, host=args.host, database=args.database, port=args.port)
        self.table_name = table_name
        self.connection_params = {
            'user': args.user,
            'password': args.password,
            'host': args.host,
            'database': args.database,
            'port': args.port
        }

    def sql(self, SQL):
        """ executes single sql statement """
        with self.conn.cursor() as curs:
            curs.execute(SQL)
        self.conn.commit()

    def insert_rows(self, rows, table_name=None):
        """
        Inserts many rows, all in the same transaction.
        """

        if table_name is None:
            table_name = self.table_name

        with self.conn.cursor() as curs:
            sql_str, template = sql.insert_many(table_name, rows)
            try:
                psycopg2.extras.execute_values(
                    curs,
                    sql_str,
                    rows,
                    template=template,
                    page_size=len(rows)
                )
            except psycopg2.DataError:
                print(rows) # useful for debugging
                raise
        self.conn.commit()

    def execute_sql_file(self, sql_file):
        """
        Executes the provided sql file.
        Assumes the path is relative to ./sql
        """
        file_path = os.path.join(os.path.dirname(__file__), 'sql', sql_file)

        with open(file_path, 'r', encoding='utf-8') as f:
            self.sql(f.read())

    def execute_and_fetchone(self, query):
        with self.conn.cursor() as curs:
            curs.execute(query)
            return curs.fetchone()[0]


    def table_exists(self, table_name):
        query = "SELECT EXISTS(SELECT 1 FROM information_schema.tables where table_name = '{0}')".format(table_name)
        return self.execute_and_fetchone(query)

    def row_count(self, table_name):
        query = "SELECT COUNT(*) from {0}".format(table_name)
        return self.execute_and_fetchone(query)

    def password_file_contents(self):
        return "{host}:{port}:{database}:{user}:{password}".format(**self.connection_params)
