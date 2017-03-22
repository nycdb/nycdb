#!/bin/bash

if [[ $NYCDB_DOCKER == true ]]; then
    if [ -f ./env.sh ];then
	mv ./env.sh ./env.sh.backup
    fi
    cp docker_env.sh env.sh
fi

if [ ! -e ./env.sh ];then
    printf "MISSING env.sh\n"
    exit 1
fi

source ./env.sh
chmod -R +x *.sh

if  [ "$1" == --pluto-all ]; then
    ./scripts/pluto.sh all
else
    ./scripts/pluto.sh
fi

./scripts/dobjobs.sh
./scripts/dof_sales.sh
./scripts/hpd_registrations.sh
./scripts/hpd_violations.sh
./scripts/rentstab.sh

python3 scripts/check_installation.py "${NYCDB_CONNECTION_STRING}"

if [ -f ./env.sh.backup ];then
    mv ./env.sh.backup ./env.sh
fi
