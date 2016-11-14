#!/bin/bash

set -e
source ./env.sh

pwd=$(pwd)
mkdir -p tmp

printf "Downloading the most recent Job Filings from NYC Open Data\n"
wget https://data.cityofnewyork.us/api/views/ic3t-wcy2/rows.csv?accessType=DOWNLOAD -O tmp/job_filings.csv
job_filings_path=${pwd}/tmp/job_filings.csv

printf "Inserting DOB data into postgres\n"
cd ${pwd}/modules/dobjobs/csvparser
python3 db_dobjobs.py $job_filings_path "${NYCDB_CONNECTION_STRING}"

# optionally add lat lng to data.
# This is not that important because lat/lng can just as easily be retrieved by joining the table with pltuo
# psql -d $NYCDB_DATABASE -f sql/geocode.sql

printf "Indexing DOB Data\n"
cd ${pwd}/modules/dobjobs/sql
execute_sql ./add_columns.sql
execute_sql ./index.sql

cd $pwd
rm tmp/* && rmdir tmp
