import asyncio
from typing import List
from datetime import datetime as dt

from pymongo.database import Database

from fp_common.mois.jumin import fetch_sido_list, fetch_population_data
from fp_common.fp_types.jumin import SidoData, SidoGroup, PopulationData
from fp_common.mongo_dao.populations import PopulationDao


async def insert_population_data(
    db: Database,
):
    pd = PopulationDao(db)
    grouped_data: SidoGroup = await fetch_sido_list()
    start_year = 2008
    end_year = dt.now().year
    year_list = list(range(start_year, end_year + 1))
    population_list = ['all']
    api_call_list = []
    semaphore = asyncio.Semaphore(10)  # Limit to 10 concurrent tasks

    async def limited_fetch_population_data(*args, **kwargs):
        async with semaphore:
            population_list: List[PopulationData] = await fetch_population_data(
                *args,
                **kwargs
            )
            code_date_list = [x['codeDatePopulationType'] for x in population_list]
            if code_date_list:
                pd.upsert_data_list_by_primary_key(
                    population_list,
                    code_date_list,
                    'codeDatePopulationType'
                )
            else:
                print('no data', args, kwargs)
    for year in year_list:
        for population_type in population_list:
            for _, levels in grouped_data.items():
                for level1dict in levels['levels1']:
                    level1dict: SidoData
                    for level2dict in levels['levels2']:
                        api_call_list.append(
                            limited_fetch_population_data(
                                level1_cd=level1dict['hangkikcd'],
                                level2_cd=level2dict['hangkikcd'],
                                population_type=population_type,
                                year=year
                            )
                        )
    await asyncio.gather(*api_call_list)
