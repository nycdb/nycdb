FROM debian:jessie
MAINTAINER ziggy

RUN apt-get update && \
    apt-get -y install build-essential \ 
    wget \ 
    python3 \
    python3-dev \ 
    python3-psycopg2 \ 
    python3.4-venv \ 
    postgresql-client \
    libpq-dev \
    unzip \
    git

RUN mkdir /opt/nyc-db

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/
