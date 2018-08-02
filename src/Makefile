VERSION := $(shell python3 setup.py --fullname)
GPG_KEYID :=  0xB95EC83A0D72CBA1

init: venv requirements.txt
	./venv/bin/pip3 install -r requirements.txt --no-binary psycopg2

test:
	pytest tests/unit/

test-unit: test

test-integration:
	docker run --name nycdb-test -p 7777:5432 -e POSTGRES_PASSWORD=password -d postgres:10.4
	./scripts/wait-for-pg.sh
	./venv/bin/pytest tests/integration || true
	docker stop nycdb-test && docker rm -v nycdb-test

venv:
	python3 -m venv venv

clean:
	rm -rf dist build nycdb.egg-info

build-requirements:
	pip3 install wheel twine

build:
	python3 setup.py sdist bdist_wheel

sign:
	gpg --detach-sign --local-user $(GPG_KEYID) -a dist/$(VERSION).tar.gz
	gpg --detach-sign --local-user $(GPG_KEYID) -a dist/$(VERSION)-py3-none-any.whl


upload:
	twine upload dist/$(VERSION).tar.gz dist/$(VERSION).tar.gz.asc
	twine upload dist/$(VERSION)-py3-none-any.whl dist/$(VERSION)-py3-none-any.whl.asc

.PHONY: init test test-integration test-unit cython build clean launch-docker
