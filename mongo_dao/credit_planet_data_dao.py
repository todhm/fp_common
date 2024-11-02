from pymongo.database import Database
from .base_dao import BaseDao


class CreditPlanetDataDao(BaseDao):

    def __init__(self, db: Database, col: str = 'credit_planet_data'):
        self.db = db
        self.col = self.db[col]
