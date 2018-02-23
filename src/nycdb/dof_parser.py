import xlrd


def cell_converter(cell):
    if cell.ctype == 0:
        return ""
    elif cell.ctype == 1:
        return cell.value.strip()
    elif cell.ctype == 2:
        return int(cell.value)
    elif cell.ctype == 3:
        return xlrd.xldate.xldate_as_datetime(cell.value, 0)
    else:
        return cell.value


def item_exists(item):
    if item is None:
        return False
    if isinstance(item, str) and item.strip() == '':
        return False
    return True


def normalize_header_str(x):
    return x.lower().replace(' ', '').replace('-', '')


def to_headers(row):
    """
    Turns data from excel row into list of lowercase list of string
    with spaces and dashes removed
    input: [xlrd.sheet.Cell]
    output: [str]
    """
    return [normalize_header_str(x) for x in map(cell_converter, row)]


def parse_dof_file(file_path):
    """ Parse dof rolling sales xls file"""
    book = xlrd.open_workbook(file_path)
    sheet = book.sheet_by_index(0)
    rows = sheet.get_rows()

    # remove first 4 row
    [next(rows) for x in range(4)]
    # 5th row is the headers
    headers = to_headers(next(rows))

    for row in rows:
        _row = list(map(cell_converter, row))

        if len(list(filter(item_exists, _row))):
            yield dict(zip(headers, _row))
