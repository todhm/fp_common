from typing import Dict
from pymongo.database import Database
from .base_dao import BaseDao


class ApartmentRealEstateDao(BaseDao):

    def __init__(self, db: Database, col: str = 'apartment_real_estate'):
        self.db = db
        self.col = self.db[col]

