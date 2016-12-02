#!/bin/bash

# Run this before or uncomment
# ./download.sh

chmod -R +x *.sh

./dobjobs.sh
./dof_sales.sh
./hpd_registrations.sh

if  [ "$1" == --pluto-all ]; then
    ./pluto.sh all
else
    ./pluto.sh
fi

./hpd_violations.sh
./rentstab.sh
