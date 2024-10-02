from typing import TypedDict, Dict, List


class Item(TypedDict):
    sggCd: str
    umdCd: str
    landCd: str
    bonbun: str
    bubun: str
    roadNm: str
    roadNmSggCd: str
    roadNmCd: str
    roadNmSeq: str
    roadNmbCd: str
    roadNmBonbun: str
    roadNmBubun: str
    umdNm: str
    aptNm: str
    jibun: str
    excluUseAr: str
    dealYear: str
    dealMonth: str
    dealDay: str
    dealAmount: str
    floor: str
    buildYear: str
    aptSeq: str
    cdealType: str
    cdealDay: str
    dealingGbn: str
    estateAgentSggNm: str
    rgstDate: str
    aptDong: str
    slerGbn: str
    buyerGbn: str
    landLeaseholdGbn: str


class ApartmentRealEstateDict(Item):
    excluUseAr: float
    dealYear: int
    dealMonth: int
    dealDay: int
    dealAmount: int
    floor: int
    buildYear: int
    code: str
    sido: str
    sigungu: str
    codeDate: str
    ymd: str


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


class RealEstateAPISalesResponse(TypedDict):
    response: Response
