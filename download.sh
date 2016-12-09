#!/bin/bash
# This downloads housing data for the database and stores the files in the 'data' folder.
# Run this with the name of a data source to download: dobjobs, dofsales, hpd
# or with 'all' to download all the data.
# you can optionly include the flag: --pluto-all
# Example: ./download.sh dofsales

set -e
pwd=$(pwd)
mkdir -p data

if [ "$1" == dobjobs ];then
    printf "Downloading the most recent Job Filings from NYC Open Data\n"
    mkdir -p data/dobjobs
    wget https://data.cityofnewyork.us/api/views/ic3t-wcy2/rows.csv?accessType=DOWNLOAD -O data/dobjobs/job_filings.csv
elif [ "$1" == dofsales ]; then
    printf "Downloading rolling sales data from the department of finance\n"
    mkdir -p data/dofsales
    cd data/dofsales
    wget http://www1.nyc.gov/assets/finance/downloads/pdf/rolling_sales/rollingsales_manhattan.xls
    wget http://www1.nyc.gov/assets/finance/downloads/pdf/rolling_sales/rollingsales_bronx.xls
    wget http://www1.nyc.gov/assets/finance/downloads/pdf/rolling_sales/rollingsales_brooklyn.xls
    wget http://www1.nyc.gov/assets/finance/downloads/pdf/rolling_sales/rollingsales_queens.xls
    wget http://www1.nyc.gov/assets/finance/downloads/pdf/rolling_sales/rollingsales_statenisland.xls
    cd $pwd
elif [ "$1" == hpd ]; then
    printf "Downloading hpd registration data\n"
    mkdir -p data/hpd
    wget http://www1.nyc.gov/assets/hpd/downloads/misc/Registrations20161201.zip -O data/hpd/registrations.zip
    printf "Unzipping hpd registration data\n"
    unzip data/hpd/registrations.zip -d data/hpd
    rm data/hpd/*.xml
elif [ "$1" == pluto ]; then

    mkdir -p data/pluto
    if  [ "$2" == --pluto-all ]; then
	./download_pluto.sh all
    else
	./download_pluto.sh recent
    fi

elif [ "$1" == violations ]; then
    
    mkdir -p data/hpd_violations && cd data/hpd_violations
    printf "Downloading HPD Violations \n"
    ${pwd}/modules/hpd-violations/download_violations.sh
    printf "Unzipping HPD Violations \n"
    ${pwd}/modules/hpd-violations/unzip.sh
    cd $pwd
    
elif [ "$1" == rentstab ]; then

    mkdir -p data/rentstab
    wget http://taxbills.nyc/joined.csv -O data/rentstab/joined.csv

elif [ "$1" == all ]; then

    ./download.sh dobjobs
    ./download.sh dofsales
    ./download.sh hpd
    ./download.sh pluto $2
    ./download.sh violations
else
    printf "Please provide which data source you would like to download. Your options are:\n"
    printf "dobjobs, dofsales, hpd, violations, rentstab or all\n"
    exit 1
fi
