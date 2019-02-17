#------------------------#
# NYC-DB                 #
#------------------------#

# CONNECTION VARIABLES
DB_HOST='127.0.0.1'
DB_DATABASE=nycdb
DB_USER=nycdb
DB_PASSWORD=nycdb
PGPASSWORD=$(DB_PASSWORD)
export PGPASSWORD

default: help

NYCDB := nycdb -D $(DB_DATABASE) -H $(DB_HOST) -U $(DB_USER) -P $(DB_PASSWORD)

datasets := $(shell nycdb --list-datasets | egrep -v 'pluto_(17v1|16v2|18v1)')

all_datasets := $(shell nycdb --list-datasets)

nyc-db: $(datasets)
	make verify

nyc-db-all: $(all_datasets)
	make verify

$(all_datasets):
	$(NYCDB) --download $@
	$(NYCDB) --load $@

verify:
	$(NYCDB) --verify-all

pg-connection-test:
	@psql -h $(DB_HOST) -U $(DB_USER) -d $(DB_DATABASE) -c "SELECT NOW()" > /dev/null 2>&1 && echo 'CONNECTION IS WORKING' || echo 'COULD NOT CONNECT'

db-shell:
	psql -h $(DB_HOST) -U $(DB_USER) -d $(DB_DATABASE)

db-dump:
	PGPASSWORD=$(DB_PASSWORD) pg_dump --no-owner --clean --if-exists -U $(DB_USER) -h $(DB_HOST) $(DB_DATABASE) > "nyc-db-$$(date +%F).sql"

db-dump-bzip:
	bzip2 --keep nyc-db*.sql


launch-docker:
	docker run --name nycdb -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres:10.3

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
	@echo '  2) create the database: make nyc-db DB_USER=YOURPGUSER DB_PASSWORD=YOURPASS'
	@echo '---------------------------------------------------------------'
	@echo 'If things get messed up try: '
	@echo ' $ sudo make remove-venv to clean the python environments'
	@echo '   or  '
	@echo ' $ sudo make clean to remove the postgres directory (and the database data!)'
	@echo 'Look at the README or Makefile for additional scripts'


.PHONY: $(datasets) nyc-db setup verify
.PHONY: db-dump db-dump-bzip pg-connection-test db-shell launch-docker
.PHONY: default help
