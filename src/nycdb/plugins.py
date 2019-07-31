from pathlib import Path
import importlib
from importlib.util import find_spec
import pkgutil


class Plugin:
    def __init__(self, name: str):
        self.name = name
        self.spec = find_spec(name)
        self.root_dir = Path(self.spec.origin).parent.resolve()

    def import_submodule(self, name: str):
        return importlib.import_module(f"{self.name}.{name}")


def iter_plugins():
    yield Plugin('nycdb')

    for finder, name, ispkg in pkgutil.iter_modules():
        if ispkg and name.startswith('nycdb_'):
            yield Plugin(name)
