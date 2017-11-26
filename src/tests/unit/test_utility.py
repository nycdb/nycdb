import nycdb

def test_mkdir(tmpdir):
    file_path = tmpdir.join('directory/file.zip')
    assert tmpdir.join('directory').check() is False
    assert file_path.check() is False
    nycdb.utility.mkdir(file_path.strpath)
    assert tmpdir.join('directory').check() is True
    assert file_path.check() is False
    # check that it can be run again without errors:
    nycdb.utility.mkdir(file_path.strpath)
    assert tmpdir.join('directory').check() is True
    assert file_path.check() is False

