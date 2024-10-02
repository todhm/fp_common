from typing import TypedDict, Literal, Optional, List


PopulationType = Literal[
    "all", "resident", "unregisteredResident", "overseasKorean"
]


class SidoData(TypedDict):
    sidonm: str
    hangkikcd: str
    levels: str


class SidoGroup(TypedDict):
    level1s: List[SidoData]
    level2s: List[SidoData]


class PopulationData(TypedDict):
    populationType: PopulationType
    level1Cd: str
    level2Cd: str
    lawCd: str
    year: int
    yearMonth: str
    codeDate: str
    codeDatePopulationType: str
    sigunguName: str
    dongName: Optional[str]
    depth: Literal[1, 2]
    totalPopulation: Optional[int]
    numHouseholds: Optional[int]
    populationPerHousehold: Optional[int]
    malePopulation: Optional[int]
    womanPopulation: Optional[int]
    manWomanRatio: Optional[float]
