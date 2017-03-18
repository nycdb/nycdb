#!/bin/bash
# ---------------------------------------------------------------- #
# Calling this script with the argument 'all' : ./pluto.sh all
# will insert many versions of PLUTO, back to 2003.
# Otherwise, it will just import the most recent version
# ---------------------------------------------------------------- #

set -e
pwd=$(pwd)

cp env.sh ./modules/pluto/pg_setup.sh
echo "pluto_root=${pwd}/data/pluto/" >> modules/pluto/pg_setup.sh

cd modules/pluto
chmod +x *.sh

# if the venv folder doesn't exist, setup it up
if [ ! -d ${pwd}/modules/pluto/venv ]; then
    printf 'Setting up python virtural environment with pyproj & cython\n'
    ./setup.sh
fi

if [[ $1 == all ]]; then
    printf "Inserting all PLUTOs\n"
    ./pluto.sh 
else
    printf "Inserting the most recent PLUTO\n"
    ./pluto16v2.sh 
fi

cd $pwd
