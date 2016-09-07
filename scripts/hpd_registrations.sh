#!/bin/bash

source env.sh

printf "***HPD Registrations***\n"

cd $HPD_REPO_PATH
mkdir -p tmp

cat ${HPD_REGISTRATIONS_FILE} | python data_cleanup.py 16 1> tmp/registrations.txt 2> tmp/registrations_errors.txt
cat ${HPD_CONTACTS_FILE} | python data_cleanup.py 15 1> tmp/contacts.txt 2> tmp/contacts_errors.txt

printf "Removed "$(cat tmp/registrations_errors.txt | wc -l)" bad lines from the registrations data\n"
printf "Removed "$(cat tmp/contacts_errors.txt | wc -l)" bad lines from the contacts data\n"

HPD_REGISTRATIONS_FILE=$(pwd)/tmp/registrations.txt
HPD_CONTACTS_FILE=$(pwd)/tmp/contacts.txt

HPD_REGISTRATIONS_FILE=$(pwd)/tmp/registrations.txt
HPD_CONTACTS_FILE=$(pwd)/tmp/contacts.txt

printf 'create table and COPY data\n'
psql -d ${NYCDB_DATABASE} -f 'sql/schema.sql'

printf 'Inserting data\n'
psql -d ${NYCDB_DATABASE} -c "COPY hpd.registrations FROM '"${HPD_REGISTRATIONS_FILE}"' (DELIMITER '|', FORMAT CSV, HEADER TRUE);"
psql -d ${NYCDB_DATABASE} -c "COPY hpd.contacts FROM '"${HPD_CONTACTS_FILE}"' (DELIMITER '|', FORMAT CSV, HEADER TRUE);"
psql -d ${NYCDB_DATABASE} -c "COPY hpd.bbl_lookup FROM '"${BBL_LAT_LNG}"' (FORMAT CSV,  HEADER TRUE);"

printf 'cleanup contact addresses\n'
psql -d ${NYCDB_DATABASE} -f 'sql/address_cleanup.sql'

printf 'cleanup registration addresses\n'
psql -d ${NYCDB_DATABASE} -f 'sql/registrations_clean_up.sql'

printf 'Add function anyarray_uniq()\n'
psql -d ${NYCDB_DATABASE} -f 'sql/anyarray_uniq.sql'

printf 'Add function anyarray_remove_null\n'
psql -d ${NYCDB_DATABASE} -f 'sql/anyarray_remove_null.sql'

printf 'Add aggregate functions first() and last()\n'
psql -d ${NYCDB_DATABASE} -f 'sql/first_last.sql'

printf 'Creating corporate_owners table\n'
psql -d ${NYCDB_DATABASE} -f 'sql/corporate_owners.sql'

printf 'Geocodes registrations via pluto\n'
psql -d ${NYCDB_DATABASE} -f 'sql/registrations_geocode.sql'

printf 'Creating table registrations_grouped_by_bbl\n'
psql -d ${NYCDB_DATABASE} -f 'sql/registrations_grouped_by_bbl.sql'

printf 'Indexing tables\n'
psql -d ${NYCDB_DATABASE} -f 'sql/index.sql'
