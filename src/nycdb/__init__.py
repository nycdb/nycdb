"""nycdb - nyc housing database"""

__version__ = '0.1.0'
__author__ = 'ziggy <ziggy@elephant-bird.net>'
__all__ = []

from .database import Database
from .downloader import Downloader
from .dataset import Dataset, File, datasets
from .transform import *

#datasets = _datasets()