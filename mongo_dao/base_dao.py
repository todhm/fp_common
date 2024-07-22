from typing import Dict, List
from pymongo.database import Database


class BaseDao(object):

    def __init__(self, db: Database, col: str):
        self.db = db
        self.col = self.db[col]

    def upsert_data_list_by_primary_key(self, data_list: List[Dict], primary_key_list: List[str], primary_key: str):
        delete_query = {primary_key: {
            "$in": primary_key_list
        }}
        self.col.delete_many(delete_query)
        self.col.insert_many(data_list)
