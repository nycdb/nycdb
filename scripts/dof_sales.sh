#!/bin/bash

source env.sh

cd $DOF_SALES_REPO
python3 insert_data.py $DOF_SALES_DATA_PATH $NYCDB_CONNECTION_STRING
printf "There are %s problem_lines\n" $(uniq problem_lines.csv | wc -l)
printf "If this number is unreasonable high (above 50) then something went wrong\n"
printf "Deleting problem_lines.csv\n"
rm problem_lines.csv
