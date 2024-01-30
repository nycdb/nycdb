import os
import subprocess
import tempfile
import zipfile


class Shapefile:
    def __init__(self, schema, connstring=None, root_dir=None):
        self.connstring = connstring
        self.table_name = schema["table_name"]
        self.path = schema["path"]
        self.zip_file = os.path.join(root_dir, schema["dest"])

    def db_import(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            zipfile.ZipFile(self.zip_file, mode="r").extractall(path=tmpdir)

            shp2pgsql = subprocess.run(
                ["shp2pgsql", os.path.join(tmpdir, self.path)],
                universal_newlines=True,
                stdout=subprocess.PIPE,
            )

            psql = subprocess.run(
                ["psql", self.connstring],
                universal_newlines=True,
                input=shp2pgsql.stdout,
            )
