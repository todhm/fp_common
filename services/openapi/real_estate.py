from pymongo.database import Database
from fp_common.openapi import openapi
from fp_common.mongo_dao import RealEstateDao


def real_estate_service(db: Database, openapi_key: str, max_number: int = 5000000):
    total_counts = openapi.fetch_realestate_total_counts()
    jump = 1000
    red = RealEstateDao(db)
    total_counts = min(total_counts, max_number)
    for i in range(0, total_counts, jump):
        result = openapi.fetch_realestate_data(
            openapi_key,
            i,
            i + jump - 1
        )
        id_list = [x['id'] for x in result]
        red.upsert_data_list_by_primary_key(
            result,
            id_list,
            'id'
        )
