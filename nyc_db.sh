#!/bin/bash

# Run this before or uncomment
# ./download.sh

if [[ $NYCDB_DOCKER == true ]]; then
    if [ -f ./.env.sh ];then
	mv ./env.sh ./env.sh.backup
    fi
    cp docker_env.sh env.sh
fi

chmod -R +x *.sh

if  [ "$1" == --pluto-all ]; then
    ./pluto.sh all
else
    ./pluto.sh
fi

./dobjobs.sh
./dof_sales.sh
./hpd_registrations.sh

./hpd_violations.sh
./rentstab.sh

if [ -f ./.env.sh.backup ];then
    mv ./env.sh.backup ./env.sh
fi
