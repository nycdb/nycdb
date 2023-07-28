def create_table(table_name, fields) -> str:
    """
    String, Iterable --> String
    """
    sql = "CREATE TABLE {} (".format(table_name)
    sql += ", ".join(["{} {}".format(field, fields[field]) for field in fields])
    sql += ")"
    return sql


def insert_many(curs, table_name, rows) -> str:
    """
    Given a psycopg.ClientCursor, a table name, and a list of dictionaries
    representing rows, generate a sql statement string that already has the
    parameters safely formatted using mogrify. This statement can be passed to
    psycopg.execute to bulk insert all the values for improved efficiency. [1]

    For example:

        >>> insert_many(curs, 'boop', [{'foo': 1, 'bar': 2}, {'foo': 3, 'bar': 4}])
        'INSERT INTO boop (foo, bar) VALUES (1,2), (3,4)'

    [1]:
    https://www.geeksforgeeks.org/format-sql-in-python-with-psycopgs-mogrify/
    """

    field_names = rows[0].keys()
    placeholder = f"({','.join(['%s' for k in field_names])})"
    fields = placeholder % tuple(field_names)
    values = ",".join(curs.mogrify(placeholder, tuple(row.values())) for row in rows)
    sql = f"INSERT INTO {table_name} {fields} VALUES {values}"

    return sql
