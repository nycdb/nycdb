import nycdb
from nycdb.file import safe_int

import time
import http.server
import io
import logging
import os
import multiprocessing
import pytest
import requests

mp = multiprocessing.get_context('fork')

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

    p = mp.Process(target=run)
    p.start()
    time.sleep(0.1)
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


# Socrata app token. These tests replace the HTTP transport with a synthetic
# one, so no request leaves the process. The token values are synthetic.

SYNTHETIC_TOKEN = 'synthetic-app-token-0000'
QUERY_URL = 'https://data.cityofnewyork.us/api/v3/views/abcd-1234/query.csv'


class SyntheticRaw(io.BytesIO):
    def __init__(self, body, fail_mid_stream=False, error=ConnectionResetError):
        super().__init__(body)
        self.fail_mid_stream = fail_mid_stream
        self.error = error
        self.reads = 0

    def read(self, amt=None, **kwargs):
        if self.fail_mid_stream and self.reads > 0:
            raise self.error('synthetic stream failure')
        self.reads += 1
        return super().read(amt)


@pytest.fixture
def transport(monkeypatch):
    """
    Records each request and answers from a {url: (status, body, headers)} map.
    """
    sent = []
    routes = {}

    def send(adapter, request, **kwargs):
        sent.append(request)
        status, body, headers = routes.get(request.url, (200, b'a,b\n1,2\n', {}))
        r = requests.Response()
        r.status_code = status
        r.headers = requests.structures.CaseInsensitiveDict(headers)
        r.raw = body if isinstance(body, SyntheticRaw) else SyntheticRaw(body)
        r.url = request.url
        r.request = request
        r.reason = 'synthetic'
        return r

    monkeypatch.setattr(requests.adapters.HTTPAdapter, 'send', send)
    monkeypatch.delenv('NYCDB_SOCRATA_APP_TOKEN', raising=False)
    return sent, routes


def test_is_socrata_query():
    assert nycdb.file.is_socrata_query(QUERY_URL)
    assert nycdb.file.is_socrata_query('https://data.ny.gov/api/v3/views/n9v6-gdp6/query.csv')
    assert nycdb.file.is_socrata_query('https://DATA.CITYOFNEWYORK.US/api/v3/views/abcd-1234/query.csv')
    assert not nycdb.file.is_socrata_query('http://data.cityofnewyork.us/api/v3/views/abcd-1234/query.csv')
    assert not nycdb.file.is_socrata_query('https://data.cityofnewyork.us:8443/api/v3/views/abcd-1234/query.csv')
    assert not nycdb.file.is_socrata_query('https://data.cityofnewyork.us.example.com/api/v3/views/abcd-1234/query.csv')
    assert not nycdb.file.is_socrata_query('https://data.cityofnewyork.us@example.com/api/v3/views/abcd-1234/query.csv')
    assert not nycdb.file.is_socrata_query('https://example.com/api/v3/views/abcd-1234/query.csv')
    assert not nycdb.file.is_socrata_query('https://data.cityofnewyork.us/api/views/abcd-1234/rows.csv')
    assert not nycdb.file.is_socrata_query('https://data.cityofnewyork.us/api/v3/views/abcd-1234/query.json')
    assert not nycdb.file.is_socrata_query('https://data.cityofnewyork.us:bad/api/v3/views/abcd-1234/query.csv')


def test_socrata_query_sends_app_token(transport, monkeypatch, tmpdir):
    sent, routes = transport
    monkeypatch.setenv('NYCDB_SOCRATA_APP_TOKEN', SYNTHETIC_TOKEN)
    dest = tmpdir.join('data/query.csv')
    assert nycdb.file.download_file(QUERY_URL, dest.strpath, hide_progress=True)
    assert len(sent) == 1
    assert sent[0].url == QUERY_URL
    assert sent[0].headers['X-App-Token'] == SYNTHETIC_TOKEN
    assert dest.read() == 'a,b\n1,2\n'


def test_app_token_not_sent_to_other_urls(transport, monkeypatch, tmpdir):
    sent, routes = transport
    monkeypatch.setenv('NYCDB_SOCRATA_APP_TOKEN', SYNTHETIC_TOKEN)
    urls = [
        'https://s3.amazonaws.com/example/file.csv',
        'http://data.cityofnewyork.us/api/v3/views/abcd-1234/query.csv',
        'https://data.cityofnewyork.us/api/views/abcd-1234/rows.csv',
        'https://data.cityofnewyork.us.example.com/api/v3/views/abcd-1234/query.csv',
        'https://data.cityofnewyork.us@example.com/api/v3/views/abcd-1234/query.csv',
        'https://data.cityofnewyork.us:8443/api/v3/views/abcd-1234/query.csv',
    ]
    for i, url in enumerate(urls):
        assert nycdb.file.download_file(url, tmpdir.join('data/{}.csv'.format(i)).strpath, hide_progress=True)
    assert len(sent) == len(urls)
    for request in sent:
        assert 'X-App-Token' not in request.headers
        assert SYNTHETIC_TOKEN not in request.url
        assert SYNTHETIC_TOKEN not in str(request.headers)


def test_socrata_redirect_is_not_followed(transport, monkeypatch, tmpdir):
    sent, routes = transport
    monkeypatch.setenv('NYCDB_SOCRATA_APP_TOKEN', SYNTHETIC_TOKEN)
    routes[QUERY_URL] = (302, b'', {'Location': 'https://example.com/elsewhere.csv'})
    dest = tmpdir.join('data/query.csv')
    with pytest.raises(nycdb.file.DownloadFailedException) as e:
        nycdb.file.download_file(QUERY_URL, dest.strpath, hide_progress=True)
    assert [r.url for r in sent] == [QUERY_URL]
    assert SYNTHETIC_TOKEN not in str(e.value)
    assert dest.check() is False


def test_legacy_redirect_is_followed(transport, tmpdir):
    sent, routes = transport
    url = 'https://s3.amazonaws.com/example/old.csv'
    routes[url] = (302, b'', {'Location': 'https://s3.amazonaws.com/example/new.csv'})
    dest = tmpdir.join('data/old.csv')
    assert nycdb.file.download_file(url, dest.strpath, hide_progress=True)
    assert [r.url for r in sent] == [url, 'https://s3.amazonaws.com/example/new.csv']
    assert dest.read() == 'a,b\n1,2\n'


def test_missing_token_warns_and_downloads(transport, tmpdir, caplog):
    sent, routes = transport
    dest = tmpdir.join('data/query.csv')
    with caplog.at_level(logging.WARNING):
        assert nycdb.file.download_file(QUERY_URL, dest.strpath, hide_progress=True)
    assert 'NYCDB_SOCRATA_APP_TOKEN is not set' in caplog.text
    assert 'X-App-Token' not in sent[0].headers
    assert dest.read() == 'a,b\n1,2\n'


def test_refused_without_token_is_not_cached(transport, tmpdir):
    sent, routes = transport
    routes[QUERY_URL] = (403, b'{"error": true}', {})
    dest = tmpdir.join('data/query.csv')
    for attempt in range(2):
        with pytest.raises(nycdb.file.DownloadFailedException) as e:
            nycdb.file.download_file(QUERY_URL, dest.strpath, hide_progress=True)
        assert 'HTTP 403' in str(e.value)
        assert 'NYCDB_SOCRATA_APP_TOKEN' in str(e.value)
        assert dest.check() is False
    assert len(sent) == 2


def test_refused_token_is_not_in_error(transport, monkeypatch, tmpdir, caplog):
    sent, routes = transport
    monkeypatch.setenv('NYCDB_SOCRATA_APP_TOKEN', SYNTHETIC_TOKEN)
    routes[QUERY_URL] = (401, b'{"error": true}', {})
    dest = tmpdir.join('data/query.csv')
    with caplog.at_level(logging.DEBUG):
        with pytest.raises(nycdb.file.DownloadFailedException) as e:
            nycdb.file.download_file(QUERY_URL, dest.strpath, hide_progress=True)
    assert 'HTTP 401' in str(e.value)
    assert SYNTHETIC_TOKEN not in str(e.value)
    assert SYNTHETIC_TOKEN not in caplog.text
    assert dest.check() is False


def test_invalid_token_is_not_sent_or_echoed(transport, monkeypatch, tmpdir):
    sent, routes = transport
    monkeypatch.setenv('NYCDB_SOCRATA_APP_TOKEN', 'synthetic token\nX-Injected: 1')
    with pytest.raises(nycdb.file.DownloadFailedException) as e:
        nycdb.file.download_file(QUERY_URL, tmpdir.join('data/query.csv').strpath, hide_progress=True)
    assert 'synthetic' not in str(e.value)
    assert sent == []


def test_http_error_is_not_saved(transport, tmpdir):
    sent, routes = transport
    url = 'https://s3.amazonaws.com/example/missing.csv'
    routes[url] = (404, b'<html>not found</html>', {})
    dest = tmpdir.join('data/missing.csv')
    with pytest.raises(nycdb.file.DownloadFailedException) as e:
        nycdb.file.download_file(url, dest.strpath, hide_progress=True)
    assert 'HTTP 404' in str(e.value)
    assert dest.check() is False


def test_failed_stream_leaves_no_file(transport, monkeypatch, tmpdir):
    sent, routes = transport
    monkeypatch.setenv('NYCDB_SOCRATA_APP_TOKEN', SYNTHETIC_TOKEN)
    routes[QUERY_URL] = (200, SyntheticRaw(b'a,b\n1,2\n', fail_mid_stream=True), {})
    dest = tmpdir.join('data/query.csv')
    with pytest.raises(nycdb.file.DownloadFailedException):
        nycdb.file.download_file(QUERY_URL, dest.strpath, hide_progress=True)
    assert dest.check() is False
    assert tmpdir.join('data/query.csv.part').check() is False


def test_interrupted_download_is_not_cached(transport, tmpdir):
    sent, routes = transport
    url = 'https://s3.amazonaws.com/example/big.csv'
    routes[url] = (200, SyntheticRaw(b'a,b\n1,', fail_mid_stream=True, error=KeyboardInterrupt), {})
    dest = tmpdir.join('data/big.csv')
    with pytest.raises(KeyboardInterrupt):
        nycdb.file.download_file(url, dest.strpath, hide_progress=True)
    assert dest.check() is False
    routes[url] = (200, b'a,b\n1,2\n', {})
    assert nycdb.file.download_file(url, dest.strpath, hide_progress=True)
    assert len(sent) == 2
    assert dest.read() == 'a,b\n1,2\n'
    assert tmpdir.join('data/big.csv.part').check() is False
