from typing import TypedDict, Literal
from fp_common.fp_types.enums.p2p.product_type import ProductType


class Funding119LinkDict(TypedDict):
    link: str
    title: str


class Funding119ProductDict(TypedDict):
    product_type: Literal[
        ProductType.COMPLEX_MORTGAGE,
        ProductType.MORTGAGE,
    ]
    product_name: str
    link: str
    principal_amount: int
    invested_amount: int
    borrower_age: int
    annual_income: int
    ltv: float
    announced_ltv: float
    interest_rate: float
    platform_fee_rate: float
    term_value: int
    detail: str
    mortgage_address: str
    exclusive_area: float
    floor_level: str
    mortgage_value: int
    priority_maximum_pledge_amount: int
    priority_amount: int
    payment_frequency_value: int = 12
    term_unit: Literal['Days', 'Months', 'Years'] = "Months"
    payment_frequency_unit: str = "Months"
    purchase_commitment: bool = False
    title_insurance: bool = False
    open_date: str
    start_date: str
