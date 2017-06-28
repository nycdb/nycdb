FROM debian:stretch
MAINTAINER ziggy

RUN apt-get update && \
    apt-get -y install build-essential \
    curl \
    wget \ 
    zip \ 
    unzip \
    bzip2 \ 
    git \
    htop \
    python \ 
    python-pip \
    python-psycopg2 \ 
    python3 \ 
    python3-dev \ 
    python3-psycopg2 \ 
    python3-venv \ 
    postgresql-client \ 
    libpq-dev \ 
    ruby \
    bundler 

RUN mkdir /opt/nyc-db

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/
