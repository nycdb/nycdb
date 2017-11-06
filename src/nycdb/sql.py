def create_table(table_name, fields):
    sql = "CREATE TABLE {} (".format(table_name)
    sql += ', '.join([ "{} {}".format(field, fields[field]) for field in fields ])
    sql += ')'
    return sql
