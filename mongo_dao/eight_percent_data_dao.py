from pymongo.database import Database
from .base_dao import BaseDao


class EightPercentDataDao(BaseDao):

    def __init__(self, db: Database, col: str = 'eight_percent_data'):
        self.db = db
        self.col = self.db[col]
