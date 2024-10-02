import json
from datetime import datetime as dt
from typing import List, Dict

import aiohttp
import ssl
from bs4 import BeautifulSoup

from fp_common.fp_types.jumin import PopulationData, PopulationType, SidoGroup, SidoData
from fp_common.fp_utils import string_utilis


async def fetch_sido_list() -> Dict[str, SidoGroup]:
    url = 'https://jumin.mois.go.kr/selectHangkikcdListAjax.do'
    ssl_context = ssl.create_default_context()
    ssl_context.set_ciphers("DEFAULT@SECLEVEL=1")
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        async with session.get(url) as response:
            response_text = await response.text()
            locations: List[SidoData] = json.loads(response_text)['locations']
            grouped_data: Dict[str, SidoGroup] = {}
            for data in locations:
                sidonm = data['sidonm']
                if sidonm not in grouped_data:
                    grouped_data[sidonm] = {'levels1': [], 'levels2': []}
                if data['levels'] == '1':
                    grouped_data[sidonm]['levels1'].append(data)
                elif data['levels'] == '2':
                    grouped_data[sidonm]['levels2'].append(data)
            return grouped_data


async def fetch_population_data(
    level1_cd: str,
    level2_cd: str,
    population_type: PopulationType,
    year: int
) -> List[PopulationData]:
    url = 'https://jumin.mois.go.kr/statMonth.do'
    ssl_context = ssl.create_default_context()
    ssl_context.set_ciphers("DEFAULT@SECLEVEL=1")
    now_year = dt.now().year
    population_map = {
        "all": ""
    }
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        data = {
            "sltOrgType": "2",
            "sltOrgLvl1": level1_cd,
            "sltOrgLvl2": level2_cd,
            "sltUndefType": population_map[population_type],
            "nowYear": str(now_year),
            "searchYearMonth": "month",
            "searchYearStart": year,
            "searchMonthStart": "01",
            "searchYearEnd": year,
            "searchMonthEnd": "12",
            "gender": "gender",
            "genderPer": "genderPer",
            "generation": "generation",
        }
        async with session.post(url, data=data) as response:
            soup = BeautifulSoup(await response.text())
            table = soup.find('table', attrs={
                'id': 'contextTable'
            })
            month_th_list = table.find('thead').find_all('tr')[0].find_all('th')
            ymd_string_list = [
                dt.strftime(dt.strptime(row.text, '%Y년 %m월'), '%Y%m')
                for row in month_th_list
                if '년' in row.text
            ]
            tr_list = table.find('tbody').find_all('tr')
            return_list = []
            for idx, row in enumerate(tr_list):
                depth = 1 if idx == 0 else 2
                total_td_list = row.find_all("td")
                name = total_td_list[1].text
                sigungu_name = None
                dong_name = None
                if depth == 1:
                    sigungu_name = name
                else:
                    dong_name = name
                data_td_list = total_td_list[2:]
                chunks = [data_td_list[i:i + 6] for i in range(0, len(data_td_list), 6)]
                for i, chunk in enumerate(chunks):
                    ymd = ymd_string_list[i]
                    total_populations = string_utilis.string_to_int(chunk[0].text)
                    num_nouseholds = string_utilis.string_to_int(chunk[1].text)
                    population_per_households = string_utilis.string_to_float(chunk[2].text)
                    male_population = string_utilis.string_to_int(chunk[3].text)
                    female_population = string_utilis.string_to_int(chunk[4].text)
                    man_woman_ratio = string_utilis.string_to_int(chunk[4].text)
                    return_list.append({
                        'populationType': population_type,
                        'level1Cd': level1_cd,
                        'level2Cd': level2_cd,
                        'lawCd': level2_cd[:5],
                        'year': year,
                        'yearMonth': ymd,
                        'sigunguName': sigungu_name,
                        'dongName': dong_name,
                        'depth': depth,
                        'totalPopulation': total_populations,
                        'numHouseholds': num_nouseholds,
                        'population_per_households': population_per_households,
                        'malePopulation': male_population,
                        'femalePopulation': female_population,
                        'manWomanRatio': man_woman_ratio,
                        'codeDate': level2_cd[:5] + ymd,
                        'codeDatePopulationType': level2_cd[:5] + ymd + population_type
                    })
        return return_list
