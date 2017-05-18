#------------------------#
# NYC-DB                 #
#------------------------#

# CONNECTION VARIABLES
DB_HOST='127.0.0.1'
DB_DATABASE=nycdb
DB_USER=nycdb
DB_PASSWORD=nycdb

# exporting allows these variables
# to be accessed in the subshells
# required for template.sh to work
export DB_HOST
export DB_DATABASE
export DB_USER
export DB_PASSWORD

# indicates if running inside a docker container
# used by task docker-run
NYCDB_DOCKER=

# use BASH as our sell
SHELL=/bin/bash

default: help

# the 'main' task that builds the database
nyc-db: prepare-docker pluto dobjobs dofsales hpd-registrations

download:
	./scripts/download.sh all

download-pluto-all:
	./scripts/download.sh all --pluto-all

.PHONY: pluto
pluto:
	./scripts/template.sh > ./modules/pluto/pg_setup.sh
	echo "pluto_root=$(shell pwd)/data/pluto/" >> modules/pluto/pg_setup.sh
	cd modules/pluto && make && ./pluto16v2.sh

JOB_FILINGS_PATH=$(shell pwd)/data/dobjobs/job_filings.csv

.ONESHELL: dobjobs
.PHONY : dobjobs
dobjobs:
	@echo "Inserting DOB data into postgres"
	set -eu
	./scripts/template.sh > ./modules/dobjobs/env.sh
	cd modules/dobjobs
	make install
	./venv/bin/dobjobs  --psql -H $(DB_HOST) -U $(DB_USER) -P $(DB_PASSWORD) -D $(DB_DATABASE) "$(JOB_FILINGS_PATH)"
	@echo "Indexing and Processing DOB Data"
	source env.sh
	execute_sql sql/geocode.sql
	execute_sql sql/add_columns.sql
	execute_sql sql/index.sql
	rm env.sh


DOF_SALES_PATH=$(shell pwd)/data/dofsales

.PHONY : dofsales
dofsales:
	@echo "***DOF ROLLING SALES***"
	./scripts/template.sh > ./modules/dof-sales/env.sh
	cd modules/dof-sales && make && bash to_postgres.sh $(DOF_SALES_PATH)

hpd-registrations:
	@echo "***HPD Registrations***"
	./scripts/template.sh > ./modules/hpd/env.sh
	./scripts/hpd_registrations.sh


.PHONY : docker-setup
docker-setup:
	mkdir -p postgres-data
	docker pull aepyornis/nyc-db:0.0.2
	docker pull postgres:9.6

docker-download:
	docker-compose run nycdb bash -c "cd /opt/nyc-db && make download"

docker-run:
	docker-compose run nycdb bash -c "cd /opt/nyc-db && make nyc-db NYCDB_DOCKER=true DB_DATABASE=postgres DB_USER=postgres DB_HOST=pg"

docker-shell:
	PGPASSWORD=nycdb psql -U postgres -h 127.0.0.1

docker-db-standalone:
	docker run --name nycdb -v "/home/zy/code/nyc-db/postgres-data:/var/lib/postgresql/data" -e POSTGRES_PASSWORD=nycdb -d -p 127.0.0.1:5432:5432  postgres:9.6

docker-dump:
	docker-compose run pg pg_dump --no-owner --clean --if-exists -h pg -U postgres --file=/opt/nyc-db/nyc-db.sql postgres 


prepare-docker: 
ifdef NYCDB_DOCKER
	@echo 'Running inside a docker container!'
	./scripts/docker_setup.sh
else
	@echo '-'
endif

nyc-db-pluto-all:
	./scripts/nyc_db.sh --pluto-all


.ONESHELL: db-dump
db-dump:
	source ./env.sh
	pg_dump --no-owner --clean --if-exists -h 127.0.0.1 -U nycdb nycdb > "nyc-db-$$(date +%F).sql"

db-dump-bzip:
	bzip2 --keep nyc-db*.sql

remove-venv:
	rm -rf modules/dof-sales/venv
	rm -rf modules/pluto/venv
	rm -rf modules/dobjobs/venv
	rm -rf modules/dof-sales/venv

.PHONY : clean
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
