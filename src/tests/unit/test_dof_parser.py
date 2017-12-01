import nycdb




def test_init():
    assert nycdb.dof_parser.DofParser('file/path').file_path == 'file/path'


