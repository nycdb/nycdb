#!/bin/bash

source env.sh

pwd=$(pwd)
mkdir -p tmp

printf "Downloading the most recent Job Filings from NYC Open Data\n"
wget https://data.cityofnewyork.us/api/views/ic3t-wcy2/rows.csv?accessType=DOWNLOAD -O tmp/job_filings.csv
job_filings_path=${pwd}/tmp/job_filings.csv

printf "Inserting DOB data into postgres\n"
# This assumes you have already created a python3 virtualenv in the csvparser folder and installed psycopg2. 
# See README.md of https://github.com/aepyornis/DOB-Jobs for more information
cd $NYCDB_DOBJOBS_CSVPARSER

source venv/bin/activate
python3 db_dobjobs.py $job_filings_path
deactivate
cd ..

# optionally add lat lng to data.
# This is not that important because lat/lng can just as easily be retrieved by joining the table with pltuo
# psql -d $NYCDB_DATABASE -f sql/geocode.sql

printf "Indexing DOB Data\n"
psql -d $NYCDB_DATABASE -f sql/add_columns.sql
psql -d $NYCDB_DATABASE -f sql/index.sql

cd $pwd
rm tmp/*
rmdir tmp
