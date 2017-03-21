#!/bin/bash

set -e
pwd=$(pwd)


printf "***HPD Violations***\n"

cp env.sh ${pwd}/modules/hpd-violations/pg_setup.sh
echo "HPD_VIOLATIONS_DATA_FOLDER=${pwd}/data/hpd_violations/data" >> ${pwd}/modules/hpd-violations/pg_setup.sh

cd ${pwd}/modules/hpd-violations
printf "Unzipping HPD Violations \n"
./unzip.sh
printf "Inserting HPD Violations \n"
./to_postgres.sh

rm ${pwd}/modules/hpd-violations/pg_setup.sh

cd ${pwd}
