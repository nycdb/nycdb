#!/bin/bash

set -e
source ./env.sh

pwd=$(pwd)
mkdir -p tmp

printf "Inserting DOB data into postgres\n"

cd ${pwd}/modules/dobjobs/csvparser
job_filings_path=${pwd}/data/dobjobs/job_filings.csv
python3 db_dobjobs.py $job_filings_path "${NYCDB_CONNECTION_STRING}"

printf "Indexing and Processing DOB Data\n"

execute_sql ${pwd}/modules/dobjobs/sql/geocode.sql
execute_sql ${pwd}/modules/dobjobs/sql/add_columns.sql
execute_sql ${pwd}/modules/dobjobs/sql/index.sql

cd ${pwd}
