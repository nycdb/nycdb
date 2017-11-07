init: venv
	pip3 install -r requirements.txt

test:
	pytest

integration-test:
	docker run --name nycdb-test -p 7777:5432 -e POSTGRES_PASSWORD=password -d postgres:10
#	pytest tests-integration/*
	docker stop nycdb-test && docker rm -v nycdb-test

venv:
	python3 -m venv venv

.PHONY: init test
