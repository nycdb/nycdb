from .dataset import Dataset, datasets


class Datasets:
    """ All NYCDB datasets """

    def __init__(self, args):
        self.args = args
        self.datasets = [Dataset(k, args=args) for k in datasets()]

    def download_all(self):
        for d in self.datasets:
            d.download_files()

    def transform_all(self):
        for d in self.datasets:
            d.transfrom_files()

    def import_all(self):
        for d in self.datasets:
            d.db_import()
