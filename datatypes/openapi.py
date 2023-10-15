from typing import TypedDict, Optional, Literal


class RealEstate(TypedDict):
    id: str
    ACC_YEAR: int
    SGG_CD: str
    SGG_NM: str
    BJDONG_CD: str
    BJDONG_NM: str
    LAND_GBN: str
    LAND_GBN_NM: str
    BONBEON: str
    BUBEON: str
    BLDG_NM: str
    DEAL_YMD: str
    OBJ_AMT: float
    BLDG_AREA: float
    TOT_AREA: float
    FLOOR: int
    RIGHT_GBN: str
    CNTL_YMD: Optional[str]
    BUILD_YEAR: int
    HOUSE_TYPE: Literal['아파트']
    REQ_GBN: Literal['중개거래']
    RDEALER_LAWDNM: str
