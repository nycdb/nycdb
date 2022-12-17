ARG PYTHON_VERSION=latest
FROM python:${PYTHON_VERSION}

RUN apt-get update && apt-get install -y postgresql-client libpq-dev
WORKDIR /nycdb/src
COPY ./src/ /nycdb/src/
RUN pip install pytest
RUN pip install -e .
ENTRYPOINT [ "python", "-m", "nycdb.cli" ]
CMD [ "--list-datasets" ]
