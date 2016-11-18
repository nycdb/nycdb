#!/bin/bash

set -e
source ./env.sh

pwd=$(pwd)
mkdir -p tmp

printf "Downloading rolling sales data from the department of finance\n"
cd tmp
wget http://www1.nyc.gov/assets/finance/downloads/pdf/rolling_sales/rollingsales_manhattan.xls
wget http://www1.nyc.gov/assets/finance/downloads/pdf/rolling_sales/rollingsales_bronx.xls
wget http://www1.nyc.gov/assets/finance/downloads/pdf/rolling_sales/rollingsales_brooklyn.xls
wget http://www1.nyc.gov/assets/finance/downloads/pdf/rolling_sales/rollingsales_queens.xls
wget http://www1.nyc.gov/assets/finance/downloads/pdf/rolling_sales/rollingsales_statenisland.xls

printf "Converting xls files to csv\n"

for f in *.xls
do
    filename=$(basename "${f}" ".xls")
    xls2csv ${f} > ${filename}.csv
done

cd ${pwd}/modules/dof-sales
python3 insert_data.py ${pwd}/tmp "${NYCDB_CONNECTION_STRING}"
printf "There are %s problem_lines\n" $(uniq problem_lines.csv | wc -l)
printf "If this number is unreasonable high (above 50) then something went wrong\n"
printf "Deleting problem_lines.csv\n"
rm problem_lines.csv
rm ${pwd}/tmp/* && rmdir ${pwd}/tmp
