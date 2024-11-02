from typing import TypedDict, Literal, Optional, Dict, List
from fp_common.fp_types.enums.p2p.product_type import ProductType


class CreditPlanetLinkDict(TypedDict):
    type: Literal["mortgage", "stock"]
    funding_amount: int
    funding_end_datetime: Optional[str]
    funding_start_datetime: str
    icon_url: str
    id: int
    is_closed: bool
    is_investable: bool
    is_notified_open_product: bool
    name: str
    product_type: str
    properties: List[Dict]
    raised_amount: int
    raised_rate: float
    repayment_type: str
    status: str


class PagePropDict(TypedDict):
    pageProps: Dict


class CreditPlanetProductDict(TypedDict):
    props: PagePropDict
    page: str
    query: Dict
    type: Literal["mortgage", "stock"]
    funding_amount: int
    funding_end_datetime: Optional[str]
    funding_start_datetime: str
    icon_url: str
    id: int
    is_closed: bool
    is_investable: bool
    is_notified_open_product: bool
    name: str
    product_type: str
    properties: List[Dict]
    raised_amount: int
    raised_rate: float
    repayment_type: str
    status: str

