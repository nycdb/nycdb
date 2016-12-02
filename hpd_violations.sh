#!/bin/bash

set -e
pwd=$(pwd)

printf "***HPD Violations***\n"

cp env.sh ./modules/hpd-violations/pg_setup.sh

all_open_violations_file="${pwd}/data/hpd_violations/data/Violation*.txt"

echo "HPD_OPEN_VIOLATIONS_FILE=${all_open_violations_file}" >> ./modules/hpd-violations/pg_setup.sh
echo "HPD_VIOLATIONS_DATA_FOLDER=${pwd}/data/hpd_violations/data" >> ./modules/hpd-violations/pg_setup.sh
echo "BBL_LAT_LNG_FILE=${pwd}/modules/hpd/bbl_lat_lng.txt" >> ./modules/hpd-violations/pg_setup.sh

cd modules/hpd-violations
./to_postgres.sh
