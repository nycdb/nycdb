import nycdb
from nycdb.file import safe_int

import time
import http.server
import os
from multiprocessing import Process

def test_file_constructor_with_dest():
    file_dict = { 'url': 'http://example.com', 'dest': 'example.csv' }
    f = nycdb.File(file_dict)
    assert f.url == 'http://example.com'
    assert f.dest == os.path.abspath('./data/example.csv')


def test_file_constructor_without_dest():
    file_dict = { 'url': 'http://example.com/test.csv' }
    f = nycdb.File(file_dict)
    assert f.dest == os.path.abspath('./data/test.csv')


def server_process(directory):
    def run():
        os.chdir(directory)
        httpd = http.server.HTTPServer( ('', 6789), http.server.SimpleHTTPRequestHandler)
        httpd.serve_forever()
    
    p = Process(target=run)
    p.start()
    time.sleep(0.01)
    return p

def test_download_file(tmpdir):
    f = tmpdir.mkdir("www").join("file.txt")
    f.write('i am a file')
    dest = tmpdir.join('data/saved_filed.txt')
    p = server_process(tmpdir.strpath)
    assert dest.check() is False
    nycdb.file.download_file('http://127.0.0.1:6789/www/file.txt', dest.strpath)
    p.terminate()
    assert dest.check() is True
    assert tmpdir.join('data').check() is True
    assert dest.read() == 'i am a file'
    # This should return True and not attempt to download the file again:
    assert nycdb.file.download_file('http://localhost:6789/www/file.txt', dest.strpath)


def test_safe_int():
    assert safe_int(None) is None
    assert safe_int('') is None
    assert safe_int('blaah') is None
    assert safe_int('15') == 15
