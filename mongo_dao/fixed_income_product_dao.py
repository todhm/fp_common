from pymongo.database import Database
from .base_dao import BaseDao


class FixedIncomeProductDao(BaseDao):

    def __init__(self, db: Database, col: str = 'fixed_income_product'):
        self.db = db
        self.col = self.db[col]
