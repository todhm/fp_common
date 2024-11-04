from datetime import datetime as dt

from mongoengine import (
    EmbeddedDocument,
)
from mongoengine.fields import (
    StringField,
    IntField,
    FloatField,
    ListField,
    DateTimeField,
    ReferenceField,
    EmbeddedDocumentField,
    BooleanField,
    PointField
)
from fp_common.fp_types.enums.p2p.company import CompanyName
from fp_common.fp_types.enums.p2p.product_type import ProductType
from fp_common.models.base import BaseModel


class AccountBalance(BaseModel):
    meta = {'indexes': ['company']}
    company = StringField(
        verbose_name='회사명',
        choices=CompanyName.choices()
    )
    amount = IntField(verbose_name='이동금액')
    balance = IntField(verbose_name='잔액')


class ExpectedPayment(EmbeddedDocument):
    payment_date = DateTimeField(verbose_name='예정 지급일', required=True)
    expected_amount = FloatField(verbose_name='예상 금액', required=True)
    total_payment = IntField(verbose_name='총 지급액', required=True)
    platform_fee = IntField(verbose_name='예상 플랫폼이용료 금액', required=True)
    tax_fee = IntField(verbose_name='예상 세금 금액', required=True)


class FixedIncomeProduct(BaseModel):
    company = StringField(
        verbose_name='회사명',
        choices=CompanyName.choices()
    )
    product_type = StringField(verbose_name='상품 타입', choices=ProductType.choices())
    product_name = StringField(verbose_name='상품명', required=True)
    link = StringField(verbose_name='상품 링크')
    principal_amount = FloatField(verbose_name='원금', required=True)
    invested_amount = FloatField(verbose_name='투자금액', required=False)
    expected_invest_amount = FloatField(verbose_name='예상 투자금액', required=False)
    borrower_age = IntField(verbose_name='대출자 나이', required=False)
    annual_income = IntField(verbose_name='대출자 연소득', required=False)
    ltv = FloatField(verbose_name='LTV', required=False)
    mtv = FloatField(verbose_name='채권최고액 기반LTV', required=False)
    announced_ltv = FloatField(verbose_name='고시담보비율', required=False)
    interest_rate = FloatField(verbose_name='이자율', required=True)
    expected_recovered_amount = FloatField(verbose_name='회수예상가액', required=False)
    expected_real_interest_rate = FloatField(verbose_name='예상 실질 이자율')
    platform_fee_rate = FloatField(verbose_name='플랫폼이용료', required=True)
    term_value = IntField(verbose_name='만기 (월 단위)', required=True)
    term_unit = StringField(verbose_name='만기 단위', choices=['Days', 'Months', 'Years'], default='Months')
    payment_frequency_value = IntField(verbose_name='지급 빈도 값', required=True)
    payment_frequency_unit = StringField(verbose_name='지급 빈도 단위', choices=['Days', 'Months', 'Years'], default='Months')
    expected_payments = ListField(EmbeddedDocumentField(ExpectedPayment))
    detail = StringField(verbose_name='상품설명')
    purchase_commitment = BooleanField(verbose_name='매입확약', required=False)
    title_insurance = BooleanField(verbose_name='권원보험', required=False)
    mortgage_address = StringField(verbose_name='담보물주소', required=False)
    exclusive_area = FloatField(verbose_name='전용면적', required=False)
    floor_level = StringField(verbose_name='층수', required=False)
    mortgage_value = IntField(verbose_name='담보물 가치', required=False)
    priority_maximum_pledge_amount = IntField(verbose_name='선순위 채권최고금액', required=False)
    priority_amount = IntField(verbose_name='선순위 대출잔액', required=False)
    etc_priority_amount = IntField(verbose_name='기타선순위 대출잔액', required=False)
    coordinates = PointField(verbose_name='좌표', required=False)
    open_date = DateTimeField(verbose_name='오픈예정일')
    start_date = DateTimeField(verbose_name='실행일')
    is_closed = BooleanField(verbose_name='상품 종료 여부', default=False)
    ts = StringField(verbose_name='timestamp', default=dt.now().strftime('%Y%m%d%H%M%S'))

    def __unicode__(self):
        return f"{self.company} {self.product_name}"


class ReceivedPayment(EmbeddedDocument):
    payment_date = DateTimeField(verbose_name='수령일', required=True)
    total_payment = IntField(verbose_name='총 지급액', required=True)
    platform_fee = IntField(verbose_name='플랫폼이용료 금액', required=True)
    tax_fee = IntField(verbose_name='세금 금액', required=True)
    amount = FloatField(verbose_name='수령 금액', required=True)


class PurchaseHistory(BaseModel):
    meta = {'indexes': ['company', 'contract_start_date', 'product']}
    product = ReferenceField(FixedIncomeProduct, verbose_name='상품', required=True)
    company = StringField(
        verbose_name='회사명',
        choices=CompanyName.choices()
    )
    amount = IntField(verbose_name='이동금액')
    purchase_reason = StringField(verbose_name='구매이유')
    contract_start_date = DateTimeField(verbose_name='지급시작일')
    expected_payments = ListField(EmbeddedDocumentField(ExpectedPayment))
    recieved_payments = ListField(EmbeddedDocumentField(ReceivedPayment))
