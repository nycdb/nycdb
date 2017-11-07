init: venv
	pip3 install -r requirements.txt

test:
	pytest tests/unit/

test-unit: test

test-integration:
	docker run --name nycdb-test -p 7777:5432 -e POSTGRES_PASSWORD=password -d postgres:10
	./scripts/wait-for-pg.sh
	pytest tests/integration
	docker stop nycdb-test && docker rm -v nycdb-test

venv:
	python3 -m venv venv

.PHONY: init test test-integration test-unit
