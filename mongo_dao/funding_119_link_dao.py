from pymongo.database import Database
from .base_dao import BaseDao


class Funding119LinkDao(BaseDao):

    def __init__(self, db: Database, col: str = 'funding_119_link'):
        self.db = db
        self.col = self.db[col]
