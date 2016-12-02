#!/bin/bash

pluto_16v2 () {
    wget https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyc_pluto_16v2%20.zip -O data/pluto/pluto_16v2.zip
    unzip data/pluto/pluto_16v2.zip -d data/pluto/16v2  # unzip
    mv data/pluto/16v2/BORO_zip_files_csv/*.csv data/pluto/16v2  # move files from nested dir
    rm -r data/pluto/16v2/BORO_zip_files_csv/ 
}

pluto_download () {
    for ver in 16v1 15v1 14v2 13v2 12v2 11v2 10v2 09v2 07c 06c 05d 04c 03c; do
	wget https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyc_pluto_${ver}.zip -O data/pluto/pluto_${ver}.zip
	unzip data/pluto/pluto_${ver}.zip -d data/pluto/${ver}  # unzip
    done
}

mkdir -p data/pluto

if [ "$1" == recent ]; then
    printf "Downloading the most recent PLUTO - 16v2\n"
    pluto_16v2
elif [ "$1" == all ]; then
    printf "Downloading (most) PLUTOs since 2003\n"
    pluto_download
    pluto_16v2
else
    echo "Please indicate if you'd like to download all or only the most recent PLUTO"
fi
