FROM python:3.5

RUN apt-get update \
  && apt-get install -y \
    postgresql-client \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /src/*.deb

COPY src/requirements.txt /nycdb/src/requirements.txt

WORKDIR /nycdb/src

RUN pip install -r requirements.txt --no-binary psycopg2

COPY src/ /nycdb/src/

RUN ls -al && pip install -e .
