from typing import Dict
from pymongo.database import Database
from .base_dao import BaseDao


class PopulationDao(BaseDao):

    def __init__(self, db: Database, col: str = 'populations'):
        self.db = db
        self.col = self.db[col]
