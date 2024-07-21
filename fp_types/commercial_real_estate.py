from typing import Dict, List, Any, TypedDict


class Item(TypedDict):
    buildYear: str
    buildingAr: str
    buildingType: str
    buildingUse: str
    buyerGbn: Any
    cdealDay: Any
    cdealType: Any
    dealAmount: str
    dealDay: str
    dealMonth: str
    dealYear: str
    dealingGbn: Any
    estateAgentSggNm: Any
    jibun: str
    landUse: str
    plottageAr: Any
    sggCd: str
    sggNm: str
    shareDealingType: Any
    slerGbn: Any
    umdNm: str
    floor: Any  # Optional field


class ResponseBody(TypedDict):
    items: Dict[str, List[Item]]
    numOfRows: str
    pageNo: str
    totalCount: str


class ResponseHeader(TypedDict):
    resultCode: str
    resultMsg: str


class Response(TypedDict):
    header: ResponseHeader
    body: ResponseBody


class CommercialAPISalesResponse(TypedDict):
    response: Response
