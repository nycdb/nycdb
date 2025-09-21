import os
import tempfile
import zipfile


class Shapefile:
    def __init__(self, schema, conn=None, root_dir=None, db_schema="public"):
        self.conn = conn
        self.table_name = schema["table_name"]
        self.path = schema["path"]
        self.srid = schema["srid"]
        self.zip_file = os.path.join(root_dir, schema["dest"])
        self.db_schema = db_schema

    def db_import(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            zipfile.ZipFile(self.zip_file, mode="r").extractall(path=tmpdir)

            shapefile_path = os.path.join(tmpdir, self.path)
            
            # It's good practice to escape the path, especially on Windows
            shapefile_path_escaped = shapefile_path.replace('\\', '\\\\')

            query = f"""
            CREATE TABLE {self.table_name} AS 
            SELECT * FROM ST_Read('{shapefile_path_escaped}');
            """
            self.conn.execute(query)