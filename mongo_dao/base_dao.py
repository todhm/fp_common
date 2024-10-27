from typing import Dict, List, Any
from pymongo.database import Database, Collection


class BaseDao(object):

    def __init__(self, db: Database, col: str):
        self.db = db
        self.col: Collection = self.db[col]

    def upsert_data_by_primary_key(self, data: Dict[str, Any], primary_key_list: List[str]):
        filter_query = {}
        for primary_key in primary_key_list:
            filter_query[primary_key] = data.get(primary_key)
        update_operation = {"$set": data}
        self.col.update_one(filter_query, update_operation, upsert=True)

    def upsert_data_list_by_primary_key(self, data_list: List[Dict], primary_key_list: List[str], primary_key: str):
        delete_query = {primary_key: {
            "$in": primary_key_list
        }}
        self.col.delete_many(delete_query)
        self.col.insert_many(data_list)

    def find_distincts(self, column: str) -> List[Any]:
        return self.col.distinct(column)

    def find_all(self, search_key: Dict[str, Any]) -> List[Any]:
        return self.col.find(search_key)
