#!/bin/bash
# This downloads housing data for the database and stores the files in the 'data' folder.
# Run this with the name of a data source to download: dobjobs, dofsales, hpd
# or with 'all' to download all the data.
# you can optionly include the flag: --pluto-all
# Example: ./download.sh dofsales

set -e
pwd=$(pwd)
mkdir -p data

pluto_16v2 () {
    mkdir -p data/pluto
    wget https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyc_pluto_16v2%20.zip -O data/pluto/pluto_16v2.zip
    unzip data/pluto/pluto_16v2.zip -d data/pluto/16v2  # unzip
    mv data/pluto/16v2/BORO_zip_files_csv/*.csv data/pluto/16v2  # move files from nested dir
    rm -r data/pluto/16v2/BORO_zip_files_csv/ 
}

historic_pluto_download () {
    for ver in 16v1 15v1 14v2 13v2 12v2 11v2 10v2 09v2 07c 06c 05d 04c 03c; do
	wget https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyc_pluto_${ver}.zip -O data/pluto/pluto_${ver}.zip
	unzip data/pluto/pluto_${ver}.zip -d data/pluto/${ver}  # unzip
    done
}

download_pluto () {
    if [ "$1" == recent ]; then
	printf "Downloading the most recent PLUTO - 16v2\n"
	pluto_16v2
    elif [ "$1" == all ]; then
	printf "Downloading (most) PLUTOs since 2003\n"
	pluto_download
	pluto_16v2
    else
	printf "Please indicate if you'd like to download all or only the most recent PLUTO\n"
    fi
}

pluto_all_flag () {
    if  [ "$1" == --pluto-all ]; then
	download_pluto all
    else
	download_pluto recent
    fi
}

dobjobs () {
    printf "Downloading the most recent Job Filings from NYC Open Data\n"
    mkdir -p data/dobjobs
    wget https://data.cityofnewyork.us/api/views/ic3t-wcy2/rows.csv?accessType=DOWNLOAD -O data/dobjobs/job_filings.csv
} 

dofsales () {
    printf "Downloading rolling sales data from the department of finance\n"
    mkdir -p data/dofsales
    wget --directory-prefix=data/dofsales/ http://www1.nyc.gov/assets/finance/downloads/pdf/rolling_sales/rollingsales_manhattan.xls
    wget --directory-prefix=data/dofsales/ http://www1.nyc.gov/assets/finance/downloads/pdf/rolling_sales/rollingsales_bronx.xls
    wget --directory-prefix=data/dofsales/ http://www1.nyc.gov/assets/finance/downloads/pdf/rolling_sales/rollingsales_brooklyn.xls
    wget --directory-prefix=data/dofsales/ http://www1.nyc.gov/assets/finance/downloads/pdf/rolling_sales/rollingsales_queens.xls
    wget --directory-prefix=data/dofsales/ http://www1.nyc.gov/assets/finance/downloads/pdf/rolling_sales/rollingsales_statenisland.xls
}


hpd () {
    printf "Downloading hpd registration data\n"
    mkdir -p data/hpd
    wget http://www1.nyc.gov/assets/hpd/downloads/misc/Registrations20170701.zip -O data/hpd/registrations.zip
    printf "Unzipping hpd registration data\n"
    unzip data/hpd/registrations.zip -d data/hpd
    rm data/hpd/*.xml
}

hpd_violations () {
    printf "Downloading HPD Violations \n"
    mkdir -p data/hpd_violations
    cd data/hpd_violations
    ${pwd}/modules/hpd-violations/download_violations.sh
    cd $pwd
}

rentstab () {
    printf "Downloading Rent Stabilization Data \n"
    mkdir -p data/rentstab
    wget https://s3.amazonaws.com/nyc-db/data/rentstab/joined.csv -O data/rentstab/joined.csv
    # wget http://taxbills.nyc/joined.csv -O data/rentstab/joined.csv
}

if [ "$1" == dobjobs ];then
    dobjobs
elif [ "$1" == dofsales ]; then
    dofsales
elif [ "$1" == hpd ]; then
    hpd
elif [ "$1" == pluto ]; then
    pluto_all_flag $2
elif [ "$1" == violations ]; then
    hpd_violations
elif [ "$1" == rentstab ]; then
    rentstab
elif [ "$1" == all ]; then
    dobjobs
    dofsales
    hpd
    pluto_all_flag $2
    hpd_violations
    rentstab
else
    printf "Please provide which data source you would like to download. Your options are:\n"
    printf "dobjobs, dofsales, pluto, hpd, violations, rentstab or all\n"
    exit 1
fi
