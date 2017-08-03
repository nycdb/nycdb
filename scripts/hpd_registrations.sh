#!/bin/bash

set -e
source modules/hpd/env.sh

pwd=$(pwd)
mkdir -p tmp/

printf "Cleaning up the data\n"
cat ${pwd}/data/hpd/Registration2017*.txt | python modules/hpd/data_cleanup.py 16 1> ${pwd}/tmp/registrations.txt 2> ${pwd}/tmp/registrations_errors.txt
cat ${pwd}/data/hpd/RegistrationContact*.txt | python modules/hpd/data_cleanup.py 15 1> ${pwd}/tmp/contacts.txt 2> ${pwd}/tmp/contacts_errors.txt

printf "Removed "$(cat ${pwd}/tmp/registrations_errors.txt | wc -l)" bad lines from the registrations data\n"
printf "Removed "$(cat ${pwd}/tmp/contacts_errors.txt | wc -l)" bad lines from the contacts data\n"

printf 'Create table \n'
execute_sql ${pwd}/modules/hpd/sql/schema.sql

printf 'Inserting data\n'

HPD_REGISTRATIONS_FILE=${pwd}/tmp/registrations.txt
HPD_CONTACTS_FILE=${pwd}/tmp/contacts.txt
BBL_LAT_LNG=${pwd}/modules/hpd/bbl_lat_lng.txt

cat $HPD_REGISTRATIONS_FILE | execute_sql_cmd "COPY hpd_registrations FROM STDIN (DELIMITER '|', FORMAT CSV, HEADER TRUE);"
cat $HPD_CONTACTS_FILE | execute_sql_cmd "COPY hpd_contacts FROM STDIN (DELIMITER '|', FORMAT CSV, HEADER TRUE);"
cat $BBL_LAT_LNG | execute_sql_cmd "COPY hpd_bbl_lookup FROM STDIN (FORMAT CSV,  HEADER TRUE);"

printf 'Cleanup contact addresses\n'
execute_sql ${pwd}/modules/hpd/sql/address_cleanup.sql

printf 'Cleanup registration addresses\n'
execute_sql ${pwd}/modules/hpd/sql/registrations_clean_up.sql

printf 'Add function anyarray_uniq()\n'
execute_sql ${pwd}/modules/hpd/sql/anyarray_uniq.sql

printf 'Add function anyarray_remove_null\n'
execute_sql ${pwd}/modules/hpd/sql/anyarray_remove_null.sql

printf "Add aggregate functions first() and last()\n"
execute_sql ${pwd}/modules/hpd/sql/first_last.sql

printf 'Creating corporate_owners table\n'
execute_sql ${pwd}/modules/hpd/sql/corporate_owners.sql

printf 'Geocodes registrations via pluto\n'
execute_sql ${pwd}/modules/hpd/sql/registrations_geocode.sql

printf 'Creating table registrations_grouped_by_bbl\n'
execute_sql ${pwd}/modules/hpd/sql/registrations_grouped_by_bbl.sql

printf 'Creating table business addresses\n'
execute_sql ${pwd}/modules/hpd/sql/business_addrs.sql

printf 'Create table registration_grouped_by_bbl_with_contacts\n'
execute_sql ${pwd}/modules/hpd/sql/registrations_grouped_by_bbl_with_contacts.sql 

printf 'Adding custom functions\n'
execute_sql ${pwd}/modules/hpd/sql/functions.sql

printf 'Indexing tables\n'
execute_sql ${pwd}/modules/hpd/sql/index.sql

printf 'Removing temporary files\n'
rm -r ${pwd}/tmp
