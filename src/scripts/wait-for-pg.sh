#!/usr/bin/env bash

ATTEMPTS=0

PG_READY='pg_isready -h 127.0.0.1 -p 7777 -U postgres --quiet'

until $PG_READY; do
    if [[ $ATTEMPTS -eq 20 ]]; then
	echo 'Postgres failed to start'
	exit 1
    fi
    ((ATTEMPTS++))
    sleep 0.5
done
