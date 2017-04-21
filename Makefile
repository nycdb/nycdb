default: help

download:
	./scripts/download.sh all

download-pluto-all:
	./scripts/download.sh all --pluto-all

docker-setup:
	mkdir -p postgres-data
	docker pull aepyornis/nyc-db:0.0.1
	docker pull postgres:9.6

docker-download:
	docker-compose run nycdb bash -c "cd /opt/nyc-db && make download"

docker-run:
	docker-compose run nycdb bash -c "NYCDB_DOCKER=true cd /opt/nyc-db && make nyc-db"

docker-shell:
	PGPASSWORD=nycdb psql -U postgres -h 127.0.0.1

docker-db-standalone:
	docker run --name nycdb -v "/home/zy/code/nyc-db/postgres-data:/var/lib/postgresql/data" -e POSTGRES_PASSWORD=nycdb -d -p 127.0.0.1:5432:5432  postgres:9.6

docker-dump:
	docker-compose run pg pg_dump --no-owner --clean --if-exists -h pg -U postgres --file=/opt/nyc-db/nyc-db.sql postgres 

nyc-db:
	./scripts/nyc_db.sh

nyc-db-pluto-all:
	./scripts/nyc_db.sh --pluto-all

.ONESHELL:
SHELL=/bin/bash
db-dump:
	source ./env.sh
	pg_dump --no-owner --clean --if-exists -h 127.0.0.1 -U nycdb nycdb > "nyc-db-$$(date +%F).sql"

db-dump-bzip:
	bzip2 --keep nyc-db*.sql

remove-venv:
	rm -rf modules/dof-sales/venv
	rm -rf modules/pluto/venv

clean: remove-venv
	rm -rf postgres-data
	docker-compose rm -f

help:
	@echo 'NYC-DB: Postgres database of housing data'
	@echo 'Copyright (C) 2017 Ziggy Mintz'
	@echo "This program is free software: you can redistribute it and/or modify"
	@echo "it under the terms of the GNU General Public License as published by"
	@echo "the Free Software Foundation, either version 3 of the License, or"
	@echo '(at your option) any later version.'
	@echo '---------------------------------------------------------------'
	@echo 'To use without docker:'
	@echo '  1) create a postgres database'
	@echo '  2) create env.sh and define psql bash functions (see README for more information)'
	@echo '  3) download the files: make download'
	@echo '  4) create the database: make nyc-db'	
	@echo '---------------------------------------------------------------'
	@echo 'To use WITH docker:'
	@echo '   1) Setup: make docker-setup'
	@echo '   2) Download: make download'
	@echo '   3) Build db: make docker-run'
	@echo
	@echo 'If things get messed up try: '
	@echo ' $ sudo make remove-venv to clean the python environments'
	@echo '   or  '
	@echo ' $ sudo make clean to remove the postgres directory (and the database data!)'
	@echo 'Look at the README or Makefile for additional scripts'
