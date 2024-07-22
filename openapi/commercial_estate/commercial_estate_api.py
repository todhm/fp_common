import asyncio
from typing import Dict, Any, List

import ssl
import aiohttp
import xmltodict
from fp_common.fp_utils.func_utils import retries

from fp_common.fp_types.commercial_real_estate import CommercialAPISalesResponse, Item


@retries(times=3)
async def fetch_page(session: aiohttp.ClientSession, url: str, params: Dict[str, str], page_no: int) -> CommercialAPISalesResponse:
    params['pageNo'] = str(page_no)
    async with session.get(url, params=params) as response:
        response_text = await response.text()
        return xmltodict.parse(response_text)


@retries(times=3)
async def fetch_all_ymd_data(
    api_key: str,
    lawd_cd: str,   # 11110
    deal_ymd: str,  # 201512
) -> List[Item]:
    url = 'https://apis.data.go.kr/1613000/RTMSDataSvcNrgTrade/getRTMSDataSvcNrgTrade'
    ssl_context = ssl.create_default_context()
    ssl_context.set_ciphers("DEFAULT@SECLEVEL=1")
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        # First, fetch the first page to get the total count
        params = {
            'LAWD_CD': lawd_cd,
            'DEAL_YMD': deal_ymd,
            'serviceKey': api_key,  # Replace with your actual API key
            'pageNo': '1'
        }
        initial_response = await fetch_page(session, url, params, 1)
        total_count = int(initial_response['response']['body']['totalCount'])
        num_of_rows = int(initial_response['response']['body']['numOfRows'])

        # Calculate the total number of pages
        total_pages = (total_count + num_of_rows - 1) // num_of_rows

        # Fetch data from all pages
        tasks = [fetch_page(session, url, params, page_no) for page_no in range(1, total_pages + 1)]
        results = await asyncio.gather(*tasks)

        # Extract and combine items from all pages
        all_items = []
        for result in results:
            items = result['response']['body']['items']['item']
            all_items.extend(items)
        return all_items
