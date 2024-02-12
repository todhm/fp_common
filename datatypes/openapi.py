from typing import Optional, Literal
from typing_extensions import TypedDict
from datetime import datetime as dt


class RealEstate(TypedDict):
    id: str
    ACC_YEAR: int
    SGG_CD: str
    SGG_NM: str
    BJDONG_CD: str
    BJDONG_NM: str
    LAND_GBN: Literal["1", "2", "3", None]
    LAND_GBN_NM: Literal["대지", "산", "블럭", None]
    BONBEON: Optional[str]
    BUBEON: Optional[str]
    BLDG_NM: Optional[str]
    DEAL_YMD: str
    DEAL_YMD_DT: dt
    OBJ_AMT: float
    BLDG_AREA: float
    TOT_AREA: float
    FLOOR: Optional[int]
    RIGHT_GBN: Optional[str]
    CNTL_YMD: Optional[str]
    BUILD_YEAR: Optional[int]
    HOUSE_TYPE: Literal['아파트', '연립다세대', '오피스텔', '단독다가구']
    REQ_GBN: Literal['중개거래', '직거래']
    RDEALER_LAWDNM: Optional[str]
