def create_table(table_name, fields):
    sql = "CREATE TABLE {} (".format(table_name)
    sql += ', '.join(["{} {}".format(field, fields[field]) for field in fields])
    sql += ')'
    return sql


def insert(table_name, row):
    fields = ', '.join(row.keys())
    placeholders = ', '.join(["%({})s".format(k) for k in row.keys()])
    sql = "INSERT INTO {table_name} ({fields}) VALUES ({values});"
    return sql.format(table_name=table_name, fields=fields, values=placeholders)
