#!/bin/bash

set -e
source ./env.sh

pwd=$(pwd)
mkdir -p tmp

printf "Inserting DOB data into postgres\n"

cd ${pwd}/modules/dobjobs/csvparser
job_filings_path=${pwd}/data/dobjobs/job_filings.csv
python3 db_dobjobs.py $job_filings_path "${NYCDB_CONNECTION_STRING}"

printf "Indexing DOB Data\n"
cd ${pwd}/modules/dobjobs/sql
execute_sql ./add_columns.sql
execute_sql ./index.sql
