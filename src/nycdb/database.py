import os
import psycopg
from . import sql


class Database:
    """
    Database connection. This is a wrapper around psycopg.connection, accessible at `.conn`
    see http://initd.org/psycopg/docs/connection.html for psycopg's documentation


    """

    def __init__(self, args, table_name=None):
        """
        args is a Namespace that must contain: user, password, database, host, and port
        """
        self.connection_params = {
            "user": args.user,
            "password": args.password,
            "host": args.host,
            "database": args.database,
            "port": args.port,
        }

        self.table_name = table_name
        self.conn = psycopg.connect(self.conninfo(), cursor_factory=psycopg.ClientCursor)

    def sql(self, SQL):
        """executes single sql statement"""
        with self.conn.cursor() as curs:
            curs.execute(SQL)
        self.conn.commit()

    def insert_rows(self, rows, table_name=None):
        """
        Inserts many rows, all in the same transaction using executemany
        """

        if table_name is None:
            table_name = self.table_name

        with self.conn.cursor() as curs:
            try:
                curs.execute(sql.insert_many(curs, table_name, rows))
            except psycopg.Error:
                print(rows)  # useful for debugging
                raise
        self.conn.commit()

    def execute_sql_file(self, sql_file):
        """
        Executes the provided sql file.
        It assumes the path is relative to ./sql
        """
        file_path = os.path.join(os.path.dirname(__file__), "sql", sql_file)

        with open(file_path, "r", encoding="utf-8") as f:
            self.sql(f.read())

    def execute_and_fetchone(self, query):
        """
        Execute the given query and returns the first row
        """
        with self.conn.cursor() as curs:
            curs.execute(query)
            return curs.fetchone()[0]

    def table_exists(self, table_name):
        """Tests if the table exists"""
        query = "SELECT EXISTS(SELECT 1 FROM information_schema.tables where table_name = '{0}')".format(
            table_name
        )
        return self.execute_and_fetchone(query)

    def row_count(self, table_name):
        """returns the row count of the table"""
        query = "SELECT COUNT(*) from {0}".format(table_name)
        return self.execute_and_fetchone(query)

    def password_file_contents(self):
        return "{host}:{port}:{database}:{user}:{password}".format(
            **self.connection_params
        )

    def conninfo(self):
        return "host={host} port={port} dbname={database} user={user} password={password}".format(
            **self.connection_params
        )
