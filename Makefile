#------------------------#
# NYC-DB                 #
#------------------------#

# CONNECTION VARIABLES
DB_HOST='127.0.0.1'
DB_DATABASE=nycdb
DB_USER=nycdb
DB_PASSWORD=nycdb
PGPASSWORD=$(DB_PASSWORD)

# exporting allows these variables
# to be accessed in the subshells
# required for template.sh to work
export DB_HOST
export DB_DATABASE
export DB_USER
export DB_PASSWORD
export PGPASSWORD

# use BASH as our shell
SHELL=/bin/bash

tasks = pluto \
	dobjobs \
	dofsales \
	hpd-registrations \
	hpd-violations \
	rentstab \
	311 \
	acris \
	hpd-complaints \
	dob-complaints \
	verify

default: help

PY-NYCDB = cd src && ./venv/bin/python3 -m nycdb.cli -D $(DB_DATABASE) -H $(DB_HOST) -U $(DB_USER) -P $(DB_PASSWORD)

datasets = pluto_16v2 \
	   dobjobs \
	   dof_sales \
	   hpd_registrations \
	   hpd_violations \
	   hpd_complaints \
	   dob_complaints \
	   rentstab

#nyc-db: $(tasks)
nyc-db: $(datasets) acris | setup
	make verify

$(datasets):
	$(PY-NYCDB) --download $@
	$(PY-NYCDB) --load $@

setup:
	cd src && make init && ./venv/bin/pip3 install -e .

verify:
	python3 ./scripts/nycdb.py -H $(DB_HOST) -U $(DB_USER) -P $(DB_PASSWORD) -D $(DB_DATABASE) --check

download:
	./scripts/download.sh all

311:
	@echo "**311 Complaints**"
	cd modules/311 && make && make run

acris: acris-download
	cd modules/acris-download && make psql_real_complete psql_personal_no_extras psql_index USER=$(DB_USER) PASS=$(DB_PASSWORD) DATABASE=$(DB_DATABASE) PSQLFLAGS="--host=$(DB_HOST)"

acris-download:
	cd modules/acris-download && make

remove-venv:
	find ./modules -type d -name 'venv' -print0 | xargs -0 -r rm -r

pg-connection-test:
	@psql -h $(DB_HOST) -U $(DB_USER) -d $(DB_DATABASE) -c "SELECT NOW()" > /dev/null 2>&1 && echo 'CONNECTION IS WORKING' || echo 'COULD NOT CONNECT'

db-shell:
	psql -h $(DB_HOST) -U $(DB_USER) -d $(DB_DATABASE)

db-dump:
	PGPASSWORD=$(DB_PASSWORD) pg_dump --no-owner --clean --if-exists -U $(DB_USER) -h $(DB_HOST) $(DB_DATABASE) > "nyc-db-$$(date +%F).sql"

db-dump-bzip:
	bzip2 --keep nyc-db*.sql

db-dump-tables:
	mkdir -v -p dump

clean: remove-venv
	rm -rf postgres-data
	type docker-compose > /dev/null 2>&1 && docker-compose rm -f || /bin/true

help:
	@echo 'NYC-DB: Postgres database of NYC housing data'
	@echo 'Copyright (C) 2017 Ziggy Mintz'
	@echo "This program is free software: you can redistribute it and/or modify"
	@echo "it under the terms of the GNU General Public License as published by"
	@echo "the Free Software Foundation, either version 3 of the License, or"
	@echo '(at your option) any later version.'
	@echo '---------------------------------------------------------------'
	@echo 'USE:'
	@echo '  1) create a postgres database: createdb nycdb'
	@echo '  2) download the files: make download'
	@echo '  3) create the database: make nyc-db DB_USER=YOURPGUSER DB_PASSWORD=YOURPASS'
	@echo '---------------------------------------------------------------'
	@echo 'If things get messed up try: '
	@echo ' $ sudo make remove-venv to clean the python environments'
	@echo '   or  '
	@echo ' $ sudo make clean to remove the postgres directory (and the database data!)'
	@echo 'Look at the README or Makefile for additional scripts'


.PHONY: $(datasets) nyc-db setup
.PHONY: download acris acris-download
.PHONY: db-dump db-dump-bzip pg-connection-test
.PHONY: clean remove-venv default help
