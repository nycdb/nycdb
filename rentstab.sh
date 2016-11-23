#!/bin/bash

set -e
source ./env.sh
pwd=$(pwd)

printf "**Rent Stabilization Unit Counts**\n"
printf "NOTICE: The data used for this module is licensed CC-BY-SA by John Krauss (github.com/talos)\n"
printf "see https://github.com/talos/nyc-stabilization-unit-counts for more information\n\n"

RENTSTAB_FILE=${pwd}/data/rentstab/joined.csv

cd modules/nyc-stabilization-unit-counts


python3 insert_rentstab.py $RENTSTAB_FILE "${NYCDB_CONNECTION_STRING}"
