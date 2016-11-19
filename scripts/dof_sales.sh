#!/bin/bash

set -e
source ./env.sh
pwd=$(pwd)

printf "Converting xls files to csv using xls2csv\n"

cd ${pwd}/data/dofsales

for f in *.xls
do
    filename=$(basename "${f}" ".xls")
    xls2csv ${f} > ${filename}.csv
done

printf "Inserting the data into postgres\n"
cd ${pwd}/modules/dof-sales
python3 insert_data.py ${pwd}/data/dofsales "${NYCDB_CONNECTION_STRING}"
printf "There are %s problem_lines\n" $(uniq problem_lines.csv | wc -l)
printf "If this number is unreasonable high (above 50) then something went wrong\n"
printf "Deleting problem_lines.csv\n"
rm problem_lines.csv
