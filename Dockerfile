FROM python:3.6-stretch

RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main' > /etc/apt/sources.list.d/pgdg.list
RUN curl -sSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update && apt-get install -y \
	postgresql-client-11 \
        libpq-dev

COPY src/requirements.txt /nycdb/src/requirements.txt

WORKDIR /nycdb/src

RUN pip install -r requirements.txt --no-binary psycopg2

COPY src/ /nycdb/src/

RUN ls -al && pip install -e .
