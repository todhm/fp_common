from pymongo.database import Database
from .base_dao import BaseDao


class Funding119DataDao(BaseDao):

    def __init__(self, db: Database, col: str = 'funding_119_data'):
        self.db = db
        self.col = self.db[col]
