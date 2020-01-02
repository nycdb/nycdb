VERSION := $(shell python3 setup.py --fullname)
GPG_KEYID :=  0xB95EC83A0D72CBA1

init: venv requirements.txt
	./venv/bin/pip3 install -r requirements.txt --no-binary psycopg2

install:
	./venv/bin/pip3 install -e .

test:
	docker run -p 127.0.0.1:7777:5432 --name nycdb_test -e POSTGRES_USER=nycdb -e POSTGRES_PASSWORD=nycdb -e POSTGRES_DB=nycdb_test -d postgres:12
	./scripts/wait-for-pg.sh
	./venv/bin/pytest || true
	docker stop nycdb_test && docker rm -v nycdb_test

test-unit:
	./venv/bin/pytest tests/unit

venv:
	python3 -m venv venv

clean:
	rm -rf dist build nycdb.egg-info

build-requirements:
	pip3 install wheel twine

build:
	python3 setup.py sdist bdist_wheel

upload:
	twine upload --sign --identity $(GPG_KEYID) dist/*

.PHONY: init test test-unit build clean upload
