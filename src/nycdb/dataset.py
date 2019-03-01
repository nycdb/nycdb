import datetime
import logging
import itertools
import os
import subprocess
from tqdm import tqdm


from . import verify
from . import dataset_transformations
from . import sql
from .database import Database
from .typecast import Typecast
from .file import File
from .utility import list_wrap, merge
from .datasets import datasets

BATCH_SIZE = 1000


class Dataset:
    """Information about a dataset"""

    def __init__(self, dataset_name, args=None):
        self.name = dataset_name
        self.args = args
        self.db = None

        if self.args:
            self.root_dir = self.args.root_dir
        else:
            self.root_dir = './data'

        self.dataset = datasets()[dataset_name]
        self.files = self._files()
        self.schemas = list_wrap(self.dataset['schema'])

    def _files(self):
        return [File(file_dict, folder=self.name, root_dir=self.root_dir) for file_dict in self.dataset['files']]


    def download_files(self):
        for f in self.files:
            f.download()


    def db_import(self):
        """
        inserts the dataset in the postgres
        output:  True | Throws
        """
        self.setup_db()
        self.create_schema()

        for schema in self.schemas:
            self.import_schema(schema)

        self.sql_files()

    def index(self):
        if 'index' in self.dataset:
            for sql_file in self.dataset['index']:
                self.db.execute_sql_file(sql_file)
        else:
            logging.debug('no index files exist for this dataset')

    def transform(self, schema):
        """
        Calls the function in dataset_transformation with the same name
        as the schema.

        If no function exists with the same name as the schema table, it tries
        to call the function with the same name as the dataset

        input: dict
        output: generator
        """
        tc = Typecast(schema)

        try:
            rows = getattr(dataset_transformations, schema['table_name'])(self)
        except AttributeError:
            rows = getattr(dataset_transformations, self.name)(self, schema)

        return tc.cast_rows(rows)

    def import_schema(self, schema):
        rows = self.transform(schema)

        pbar = tqdm(unit='rows')
        while True:
            batch = list(itertools.islice(rows, 0, BATCH_SIZE))
            if len(batch) == 0:
                break
            else:
                pbar.update(len(batch))
                self.db.insert_rows(batch, table_name=schema['table_name'])
        pbar.close()

    def create_schema(self):
        create_table = lambda name, fields: self.db.sql(sql.create_table(name, fields))

        for s in self.schemas:
            create_table(s['table_name'], s['fields'])

    def sql_files(self):
        if 'sql' in self.dataset:
            for f in self.dataset['sql']:
                self.db.execute_sql_file(f)

    def setup_db(self):
        if self.db is None:
            self.db = Database(self.args, table_name=self.name)

    def verify(self):
        self.setup_db()
        verify.check_dataset(self.db, self.name)

    def dump(self):
        """Creates .sql dump file of the datasets"""
        tables = ['--table={}'.format(s['table_name']) for s in self.schemas]
        file_arg = '--file=./{}-{}.sql'.format(self.name, datetime.date.today().isoformat())
        cmd = ["pg_dump", "--no-owner", "--clean", "--if-exists", "-w"] + tables + [file_arg]
        subprocess.run(cmd, env=self.pg_env(), check=True)

    def pg_env(self):
        return merge(
            os.environ.copy(),
            {
                'PGHOST': self.args.host,
                'PGPORT': self.args.port,
                'PGUSER': self.args.user,
                'PGDATABASE': self.args.database,
                'PGPASSWORD': self.args.password
            })
