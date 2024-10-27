from pymongo.database import Database
from .base_dao import BaseDao


class EightPercentLinkDao(BaseDao):

    def __init__(self, db: Database, col: str = 'eight_percent_link'):
        self.db = db
        self.col = self.db[col]
