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


def insert_many(table_name, rows, cursor):
    '''
    Generate a literal postgres string that inserts the given rows as
    a single SQL statement. Note that this should be passed as a
    single argument to cursor.execute(): no second argument needs to
    be passed, as the string returned by this function does not include
    placeholders, for reasons of efficiency [1].

    [1]: https://stackoverflow.com/a/10147451
    '''

    field_names = list(rows[0].keys())
    fields = ', '.join(field_names)
    placeholders = ', '.join(["%({})s".format(k) for k in field_names])
    actual_values = b', '.join(cursor.mogrify('(' + placeholders + ')', row) for row in rows)
    sql = f"INSERT INTO {table_name} ({fields}) VALUES ".encode('ascii')
    return sql + actual_values
