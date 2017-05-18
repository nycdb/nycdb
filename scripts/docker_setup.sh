#!/bin/bash

if [ -f ./env.sh ];then
    mv ./env.sh ./env.sh.backup
fi

cp docker_env.sh env.sh

if [ ! -e ./env.sh ];then
    printf "MISSING env.sh\n"
    exit 1
fi

source ./env.sh
