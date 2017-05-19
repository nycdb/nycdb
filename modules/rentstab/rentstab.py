import argparse
import datetime
import decimal
import csv
import re
import psycopg2

parser = argparse.ArgumentParser(description='inserts rent stabilization data into postgres')
parser.add_argument('file', help='path to csv file')
parser.add_argument("-U", "--user", help="Postgres user. default: postgres", default="postgres")
parser.add_argument("-P", "--password", help="Postgres password. default: postgres", default="postgres")
parser.add_argument("-H", "--host", help="Postgres host: default: 127.0.0.1", default="127.0.0.1")
parser.add_argument("-D", "--database", help="postgres database: default: postgres", default="postgres")
args = parser.parse_args()

schema_file = 'nyc_stabilization_unit_counts.sql'
table_name = 'rentstab'
csv_file = args.file

conn = psycopg2.connect(user=args.user, password=args.password, host=args.host, database=args.database)
cur = conn.cursor()

total = 0
field_errors = 0
errors = []

class TypeCastError(TypeError):
    pass

# string -> int
def char_num(datatype):
    m = re.match("char\(([0-9]+)\)", datatype)
    if m:
        return int(m.group(1))
    else:
        raise Exception("datatype failed to match char regex: " + datatype)


def line_boolean(line):
    if 'char' in line:
        return True
    elif '(' in line:
        return False
    elif ')' in line:
        return False
    else:
        return True


# string -> (dict, list)
def sql_type_dir(sql_file):
    d = {}
    headers = []
    with open(sql_file, 'r') as f:
        for line in f:
            if line_boolean(line):
                key = line.strip().replace(',', '').split(' ')[0]
                val = ' '.join(line.strip().replace(',', '').split(' ')[1:])
                d[key] = val
                headers.append(key)
    return (d, headers)

def create_table(cur, tablename, schema_file):
    cur.execute('DROP TABLE IF EXISTS ' + tablename)
    with open(schema_file, 'r') as f:
        sql = f.read()
        cur.execute(sql)


def char_error(value, datatype):
    error_message = 'Schema Mismatch. ' + value + ' is ' + str(len(value)) + ' chars long. Excepted it to be ' + str(char_num(datatype))
    raise TypeCastError(error_message)

# input format: mm/dd/yyyy
# datetime.date(year, month, day)
def date_format(datestring):
    month, day, year =  [int(x) for x in datestring.split('/')]
    return datetime.date(year, month, day)


def type_cast(key, val, lookup):
    datatype = lookup[key].strip()
    value = val.strip()
    if value == '':
        return None
    elif datatype == 'text':
        return value
    elif 'char' in datatype:
        if len(value) == char_num(datatype):
            return value
        else:
            char_error(value, datatype)
    elif datatype in ['integer', 'bigint', 'smallint']:
        return int(value)
    elif datatype == 'money':
        return value.replace('$', '')
    elif datatype == 'boolean':
        return bool(value)
    elif datatype == 'date':
        return date_format(value)
    elif datatype == 'numeric':
        return decimal.Decimal(value)
    elif '[]' in datatype:
        return value.split(',')
    else:
        raise Exception('Type Cast Error - Unknown datatype - ' + datatype)


def skip(lines, f):
    for x in range(lines):
        next(f)


def placeholders(num):
    text = '('
    for x in range(num):
        if x < (num - 1):
            text += '%s, '
        else:
            text += '%s)'

    return text


def make_query(tablename, row):
    fieldnames = []
    values = []
    for key in row:
        fieldnames.append(key)
        values.append(row[key])
    query = "INSERT INTO " + tablename + " " + str(tuple(fieldnames))
    query += " values " + placeholders(len(fieldnames))
    query = query.replace("'", "")
    return (query, tuple(values))


def handle_field_error(row, key, e):
    print(key + " - " + str(row[key]))
    print(e)
    field_errors += 1
    row[key] = None


lookup, headers = sql_type_dir(schema_file)

def insert_row(row, table_name=table_name):
    for key in row:
        try:
            row[key] = type_cast(key, row[key], lookup)
        except TypeCastError as e:
            handle_field_error(row, key, e)
        except ValueError as e:
            handle_field_error(row, key, e)

    query, data = make_query(table_name, row)

    try:
        cur.execute(query, data)
    except Exception as e:
        print("Inserting Row error with: " + str(row))
        raise


def copy_data(csv_file, headers):
    with open(csv_file, 'r') as f:
        next(f)  # skip first row
        csvreader = csv.DictReader(f, fieldnames=headers)
        for row in csvreader:
            try:
                insert_row(row)
                conn.commit()
                total += 1
            except Exception as e:
                errors.append(row)
                raise

if __name__ == "__main__":
    create_table(cur, table_name, schema_file)
    copy_data(csv_file, headers)
    print('total inserted: ' + str(total))
    print('fields with errors: ' + str(field_errors))
    print('lines with errors: ' + str(len(errors)))

    if len(errors) > 0:
        with open('problem_lines.csv', 'w') as f:
            for line in errors:
                f.write(str(line) + "\n")
        print('problem_lines.csv saved!')
