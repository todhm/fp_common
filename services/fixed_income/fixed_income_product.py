from datetime import datetime, timedelta

from mongoengine import Q

from fp_common.repositories.fixed_income.fixed_income_product import FixedIncomeProductRepository
from fp_common.services.fixed_income.expected_payment_services import ExpectedPaymentService
from fp_common.fp_types.p2pproducts.eight_percent import EightPercentProductDict
from fp_common.fp_types.p2pproducts.funding119 import Funding119ProductDict
from fp_common.models.fixed_income.fixed_income import FixedIncomeProduct
from fp_common.fp_types.enums.p2p.company import CompanyName
from fp_common.fp_types.enums.p2p.product_type import ProductType
from fp_common.fp_utils import string_utilis


class FixedIncomeProductService(object):

    @classmethod
    def upsert_expected_payments(
        cls,
        fixed_income_id: str,
    ) -> FixedIncomeProduct:
        fixed_income_product = FixedIncomeProductRepository.find_by_id(fixed_income_product_id=fixed_income_id)
        ExpectedPaymentService.upsert_expected_payments_with_product(
            fixed_income_product=fixed_income_product,
        )

    @classmethod
    def upsert_from_eightpercent_dict(
        cls,
        eight_percent_dict: EightPercentProductDict,
    ) -> FixedIncomeProduct:
        category_map = {
            "stockPurchase": ProductType.STOCK.value,
            "realEstate": ProductType.MORTGAGE.value,
        }
        link_map = {
            "stockPurchase": "https://8percent.kr/deals/stock-purchase/",
            "realEstate": "https://8percent.kr/deals/real-estate-special/",
        }
        converted_data = {
            "company": CompanyName.EIGHT_PERCENT.value,
            "product_type": category_map.get(eight_percent_dict.get("category")),
            "product_name": eight_percent_dict.get("title"),
            "link": link_map.get(eight_percent_dict.get("category")) + str(eight_percent_dict.get("id")),
            "principal_amount": eight_percent_dict['dealApplication']['finalAmountWon'],
            "invested_amount": eight_percent_dict['totalAmountInvestments'],
            "borrower_age": string_utilis.date_string_to_age(
                eight_percent_dict['dealApplication']['userBorn'], '%Y-%m-%d'
            ),
            "annual_income": eight_percent_dict['dealApplication']['borrowerMonthIncome'] * 12,
            "expected_invest_amount": 5000000,
            "interest_rate": eight_percent_dict['earningRate'],
            "platform_fee_rate": eight_percent_dict['commissionRate'],
            "term_value": eight_percent_dict['length'],
            "term_unit": 'Months',
            "payment_frequency_value": 1,
            "payment_frequency_unit": 'Months',
            "purchase_commitment": eight_percent_dict['isPledgeEstablishable'],
            "title_insurance": any([row['title'] == '권원보험' for row in eight_percent_dict['sellingPoints']]),
            "open_date": datetime.strptime(eight_percent_dict['startDatetime'], '%Y-%m-%dT%H:%M:%S+09:00'),
            "start_date": max(
                datetime.strptime(eight_percent_dict['startDatetime'], '%Y-%m-%dT%H:%M:%S+09:00'),
                datetime.now()
            ) + timedelta(days=2),
        }
        if eight_percent_dict.get('category') == 'realEstate':
            converted_data.update({
                "coordinates": [
                    float(eight_percent_dict['dealApplication']['mortgage']['longitude']),
                    float(eight_percent_dict['dealApplication']['mortgage']['latitude']),
                ],
                "expected_recovered_amount": eight_percent_dict['dealApplication']['mortgage']['expectedRecoverAmount'],
                "ltv": eight_percent_dict['dealApplication']['mortgage']['loanAmountBaseLtv'],
                "announced_ltv": eight_percent_dict['dealApplication']['mortgage']['maxBondAmountBaseLtv'],
                "mortgage_address": eight_percent_dict['dealApplication']['mortgage']['address'],
                "exclusive_area": float(eight_percent_dict['dealApplication']['mortgage']['usingArea']),
                "floor_level": eight_percent_dict['dealApplication']['mortgage']['floors'],
                "mortgage_value": int(eight_percent_dict['dealApplication']['mortgage']['appraisedValue']),
                "priority_maximum_pledge_amount": int(eight_percent_dict['dealApplication']['mortgage']['priorityAmount']),
                "priority_amount": int(eight_percent_dict['dealApplication']['mortgage']['priorityLoanAmount']),
                "etc_priority_amount": int(eight_percent_dict['dealApplication']['mortgage']['etcAmount']),
            })
        upsert_condition = Q(link=converted_data["link"])
        _ = FixedIncomeProduct.objects(upsert_condition).update_one(
            upsert=True, **converted_data
        )
        fip = FixedIncomeProduct.objects.get(upsert_condition)
        cls.upsert_expected_payments(fixed_income_id=fip.id)
        return fip

    @classmethod
    def upsert_funding_119_dict(
        cls,
        funding_dict: Funding119ProductDict,
    ) -> FixedIncomeProduct:
        upsert_condition = Q(link=funding_dict["link"])
        funding_dict["expected_invest_amount"] = 5000000
        _ = FixedIncomeProduct.objects(upsert_condition).update_one(
            upsert=True, **funding_dict
        )
        fip = FixedIncomeProduct.objects.get(upsert_condition)
        cls.upsert_expected_payments(fixed_income_id=fip.id)
        return fip
