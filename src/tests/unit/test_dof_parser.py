import nycdb
import os

def test_parse_dof_file():
    file_path = os.path.join(os.path.dirname(__file__), './rollingsales_brooklyn.xls')
    dof_file =  list(nycdb.dof_parser.parse_dof_file(file_path))
    print(dof_file[-1])
    assert len(dof_file) == 100
    assert dof_file[0]['address'].strip() == '253 PACIFIC STREET'



