import os
import duckdb


class Database:
    """
    Database connection. This is a wrapper around duckdb.connect, accessible at .conn
    """

    def __init__(self, args, table_name=None):
        """
        args is a Namespace that must contain: db_path
        """
        self.db_path = getattr(args, 'db_path', 'nycdb.duckdb')
        self.table_name = table_name
        self.conn = duckdb.connect(self.db_path)
        self.conn.execute("INSTALL spatial;")
        self.conn.execute("LOAD spatial;")

    def sql(self, SQL):
        """executes single sql statement"""
        self.conn.execute(SQL)

    def insert_rows(self, file_path, table_name=None):
        """
        Bulk inserts rows from a file path.
        """

        if table_name is None:
            table_name = self.table_name

        self.conn.execute(f"COPY {table_name} FROM '{file_path}' (AUTO_DETECT TRUE)")

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
        return self.conn.execute(query).fetchone()[0]

    def table_exists(self, table_name):
        """Tests if the table exists"""
        query = f"SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}'"
        return self.conn.execute(query).fetchone() is not None

    def row_count(self, table_name):
        """returns the row count of the table"""
        query = f"SELECT COUNT(*) from {table_name}"
        return self.execute_and_fetchone(query)