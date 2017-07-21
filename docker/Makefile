# CONNECTION VARIABLES
DB_HOST=pg
DB_DATABASE=nycdb
DB_USER=nycdb
DB_PASSWORD=nycdb
PGPASSWORD=$(DB_PASSWORD)

NYCDB_DOCKER_VERSION := 0.1
SQLPAD_DOCKER_VERSION := 0.1

default:
	@echo 'NYC-DB: docker edition'
	@echo 'USE:'
	@echo '   1) Setup: make docker-setup'
	@echo '   2) Download: make docker-download'
	@echo '   3) Build db: make docker-run'

build-nycdb-docker:
	docker build -t aepyornis/nyc-db:$(NYCDB_DOCKER_VERSION) -f nycdb.docker .

build-sqlpad-docker:
	docker build -t aepyornis/nyc-db-sqlpad:$(SQLPAD_DOCKER_VERSION) -f sqlpad.docker .

docker-setup:
	mkdir -p postgres-data
	docker pull aepyornis/nyc-db:0.1
	docker pull aepyornis/nyc-db-sqlpad:0.1
	docker pull adminer:latest
	docker pull postgres:9.6
	docker pull begriffs/postgrest:v0.4.2.0

NYCDB_BASH = docker-compose run nycdb bash

docker-download:
	$(NYCDB_BASH) -c "cd /opt/nyc-db && make download"

docker-run:
	$(NYCDB_BASH) -c "PGPASSWORD=nycdb psql -U postgres -h pg -c \"CREATE USER nycdb WITH PASSWORD 'nycdb' SUPERUSER\" || true";
	$(NYCDB_BASH) -c "PGPASSWORD=nycdb psql -U nycdb -h pg -d postgres -c 'CREATE DATABASE nycdb OWNER nycdb' || true"
	$(NYCDB_BASH) -c "PGPASSWORD=nycdb psql -U nycdb -h pg -d nycdb -f /opt/nyc-db/docker/users.sql || true"
	$(NYCDB_BASH) -c "cd /opt/nyc-db && make nyc-db DB_HOST=pg"

docker-psql-shell:
	PGPASSWORD=$(DB_PASSWORD) psql -U postgres -h 127.0.0.1 -d postgres

docker-dump:
	docker-compose run pg pg_dump --no-owner --clean --if-exists -h pg -U postgres --file=/opt/nyc-db/nyc-db.sql nycdb

.PHONY: docker-setup docker-download docker-run docker-psql-shell docker-db-standalone docker-dump
