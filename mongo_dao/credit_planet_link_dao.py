from pymongo.database import Database
from .base_dao import BaseDao


class CreditPlanetLinkDao(BaseDao):

    def __init__(self, db: Database, col: str = 'credit_planet_link'):
        self.db = db
        self.col = self.db[col]
