def create_table(table_name, fields):
    sql = "CREATE TABLE {} (".format(table_name)
    sql += ', '.join(["{} {}".format(field, fields[field]) for field in fields])
    sql += ')'
    return sql


def insert(table_name, row):
    '''
    Generate a psycopg2-friendly string that uses placeholders to
    insert the given row into the database.  This can be passed to
    cursor.execute() as its first parameter; you'll want to pass the
    row itself as the second parameter.
    '''

    fields = ', '.join(row.keys())
    placeholders = ', '.join(["%({})s".format(k) for k in row.keys()])
    sql = "INSERT INTO {table_name} ({fields}) VALUES ({values});"
    return sql.format(table_name=table_name, fields=fields, values=placeholders)


def insert_many(table_name, rows):
    '''
    Given a table name and a list of dictionaries representing
    rows, generate a (sql, template) tuple of strings that can be
    passed to psycopg2.extras.execute_values() [1] to bulk insert all the
    values for improved efficiency [2].

    [1]: http://initd.org/psycopg/docs/extras.html#psycopg2.extras.execute_values
    [2]: https://stackoverflow.com/a/30985541
    '''

    field_names = list(rows[0].keys())
    fields = ', '.join(field_names)
    placeholders = ', '.join(["%({})s".format(k) for k in field_names])
    template = f"({placeholders})"
    sql = f"INSERT INTO {table_name} ({fields}) VALUES %s"

    return sql, template
