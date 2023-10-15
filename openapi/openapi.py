import requests
import xmltodict 
from typing import List
from fp_common.datatypes.openapi import RealEstate
from copy import deepcopy


def fetch_realestate_total_counts() -> int:
    url = 'http://openapi.seoul.go.kr:8088/sample/xml/tbLnOpendataRtmsV/0/5/'
    results = xmltodict.parse(requests.get(url).text)
    counts = int(results['tbLnOpendataRtmsV']['list_total_count'])
    return counts
    

def fetch_realestate_data(api_key: str, start_number: int, end_number: int) -> List[RealEstate]:
    url = f'http://openapi.seoul.go.kr:8088/{api_key}/xml/tbLnOpendataRtmsV/{start_number}/{end_number}/'
    results = xmltodict.parse(requests.get(url).text)
    data_list = results['tbLnOpendataRtmsV']['row']
    row_list = []
    for row in data_list:
        new_row = deepcopy(row)
        new_row['id'] = (
            f"{new_row['ACC_YEAR']}-{new_row['SGG_CD']}-{new_row['BJDONG_CD']}-{new_row['LAND_GBN']}-"
            f"{new_row['BONBEON']}-{new_row['FLOOR']}-{new_row['DEAL_YMD']}"
        )
        new_row['ACC_YEAR'] = int(new_row['ACC_YEAR'])
        new_row['OBJ_AMT'] = float(new_row['OBJ_AMT'])
        new_row['BLDG_AREA'] = float(new_row['BLDG_AREA'])
        new_row['TOT_AREA'] = float(new_row['TOT_AREA'])
        new_row['FLOOR'] = int(new_row['FLOOR']) if new_row.get("FLOOR") else None
        row_list.append(new_row)
    return row_list
