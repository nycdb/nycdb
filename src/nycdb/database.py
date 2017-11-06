import psycopg2

class Database:
    """Database connection to NYCDB"""

    def __init__(self, args):
        self.conn = psycopg2.connect(user=args.user, password=args.password, host=args.host, database=args.database)

    def sql(self, SQL):
        with conn.cursor() as curs:
            curs.execute(SQL)
        self.conn.commit()
