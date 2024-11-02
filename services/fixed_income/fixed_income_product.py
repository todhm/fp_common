from datetime import datetime, timedelta

from mongoengine import Q

from fp_common.repositories.fixed_income.fixed_income_product import FixedIncomeProductRepository
from fp_common.services.fixed_income.expected_payment_services import ExpectedPaymentService
from fp_common.fp_types.p2pproducts.credit_planet import CreditPlanetProductDict, CreditPlanetLinkDict
from fp_common.fp_types.p2pproducts.eight_percent import EightPercentProductDict
from fp_common.fp_types.p2pproducts.funding119 import Funding119ProductDict
from fp_common.models.fixed_income.fixed_income import FixedIncomeProduct
from fp_common.fp_types.enums.p2p.company import CompanyName
from fp_common.fp_types.enums.p2p.product_type import ProductType
from fp_common.fp_utils import string_utilis, dict_utils


class FixedIncomeProductService(object):

    @classmethod
    def close_time_passed_products(cls, ts: str):
        FixedIncomeProduct.objects.filter(ts__ne=ts).update(is_closed=True)

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
        if '전월세' in eight_percent_dict.get("title"):
            converted_data["product_type"] = ProductType.RENTAL_DEPOSIT.value
            converted_data.update({
                "coordinates": [
                    float(eight_percent_dict['dealApplication']['rentalDepositCollateral']['longitude']),
                    float(eight_percent_dict['dealApplication']['rentalDepositCollateral']['latitude']),
                ],
                "ltv": eight_percent_dict['dealApplication']['rentalDepositCollateral']['priorityLoanAmountBaseLtv'],
                "mortgage_address": eight_percent_dict['dealApplication']['rentalDepositCollateral']['address'],
                "mortgage_value": int(eight_percent_dict['dealApplication']['rentalDepositCollateral']['rentalDepositAmount']),
                "priority_amount": int(eight_percent_dict['dealApplication']['rentalDepositCollateral']['priorityLoanAmount']),
                "etc_priority_amount": 0,
            })

        elif eight_percent_dict.get('category') == 'realEstate':
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
        funding_dict["company"] = CompanyName.FUNDING_119.value
        _ = FixedIncomeProduct.objects(upsert_condition).update_one(
            upsert=True, **funding_dict
        )
        fip = FixedIncomeProduct.objects.get(upsert_condition)
        cls.upsert_expected_payments(fixed_income_id=fip.id)
        return fip
    
    @classmethod
    def upsert_from_credit_planet_dict(
        cls,
        credit_planet_dict: CreditPlanetProductDict,
    ) -> FixedIncomeProduct:
        category_map = {
            "아파트": ProductType.MORTGAGE.value,
            "증권": ProductType.STOCK.value,
            "초단기 투자": ProductType.SALES.value
        }
        category = credit_planet_dict['props']['pageProps']['pageDatas'][0]['property']['subTitle']
        product_type = category_map.get(category)
        page_list = credit_planet_dict['props']['pageProps']['pageDatas']
        base_dict = [item for item in page_list if item['componentType'] == 'TitleCard'][0]
        amount_dict = [
            row for row in base_dict['property']['children']
            if row.get("property") and row.get("property").get("targetAmount")
        ][0]
        borrower_dict = list(
            filter(
                lambda x: x.get("property") 
                and x['property'].get("title") 
                and '차입자' in x['property'].get('title'),
                page_list
            )
        )[0]
        if product_type == ProductType.SALES.value:
            annual_income = [
                string_utilis.korean_string_to_int(row["property"]["content"])
                for row in
                borrower_dict['property']['children']
                if row.get("property") and row.get("property").get("title") and (
                    '연매출' in row['property']['title']
                )
            ][0]
            borrower_age = None
        else:
            annual_income = [
                string_utilis.string_to_int(row["property"]["content"])
                for row in
                borrower_dict['property']['children']
                if row.get("property") and row.get("property").get("title") and (
                    '연소득' in row['property']['title']
                )
            ][0]
            borrower_age = [
                string_utilis.string_to_int(row["property"]["content"])
                for row in
                borrower_dict['property']['children']
                if row.get("property") and row.get("property").get("title") and '연령' in row['property']['title']
            ][0]

        investment_dict = list(
            filter(
                lambda x: x.get("property") 
                and x['property'].get("title") 
                and '투자 수익' in x['property'].get('title'), page_list
            )
        )[0]
        interest_rate = [
            string_utilis.string_to_float(row["property"]["content"])
            for row in
            investment_dict['property']['children'][0]['property']['children']
            if row.get("property") and row.get("property").get("title") and 
            '예상 수익률' in row['property']['title']
        ][0]

        platform_fee_rate = string_utilis.string_to_float(
            dict_utils.DictUtil.find_value_by_regex(investment_dict, r'플랫폼 이용료\(.*\%')
        )
        length_value = dict_utils.DictUtil.find_by_key(base_dict, 'secondTitle')['secondContent']
        term_value = string_utilis.string_to_int(length_value)
        term_unit = "Months" if '개월' in length_value else "Days"
        payment_frequency_value = 1 if term_unit == "Months" else term_value
        title_insurance_exists = dict_utils.DictUtil.find_value_by_regex(base_dict, r'title_insurance')
        title_insurance = True if title_insurance_exists is not None else False
        purchase_commitment_exists = dict_utils.DictUtil.find_value_by_regex(base_dict, r'purchase_commitment')
        purchase_commitment = True if purchase_commitment_exists is not None else False
        open_date = datetime.strptime(
            credit_planet_dict['funding_start_datetime'], '%Y-%m-%dT%H:%M:%S'
        )
        start_date = open_date if term_unit == "Days" else open_date + timedelta(days=2)
        converted_data = {
            "company": CompanyName.CREDIT_PLANET.value,
            "product_type": product_type,
            "product_name": credit_planet_dict['props']['pageProps']['pageDatas'][0]['property']['title'],
            "link": f"https://www.cple.co.kr/investing/detail/{credit_planet_dict['query']['id']}",
            "principal_amount": amount_dict["property"]["targetAmount"],
            "invested_amount": amount_dict["property"]["accumulatedAmount"],
            "borrower_age": borrower_age,
            "annual_income": annual_income,
            "expected_invest_amount": 5000000,
            "interest_rate": interest_rate,
            "platform_fee_rate": platform_fee_rate,
            "term_value": term_value,
            "term_unit": term_unit,
            "payment_frequency_value": payment_frequency_value,
            "payment_frequency_unit": term_unit,
            "purchase_commitment": purchase_commitment,
            "title_insurance": title_insurance,
            "open_date": open_date,
            "start_date": max(
                start_date,
                datetime.now()
            ),
        }
        if product_type == ProductType.MORTGAGE.value:
            mortgage_info = list(
                filter(
                    lambda x: x.get("property") 
                    and x['property'].get("title") 
                    and '담보물 상세' in x['property'].get('title'), page_list
                )
            )[0]
            mortgage_value_info = list(
                filter(
                    lambda x: x.get("property") 
                    and x['property'].get("title") 
                    and '담보물 평가' in x['property'].get('title'), page_list
                )
            )[0]
            mortgage_address = dict_utils.DictUtil.find_by_key(mortgage_info, r'location')['location']
            ltv = string_utilis.string_to_float(
                dict_utils.DictUtil.find_dict_by_value_regex(mortgage_value_info, r"유효담보")['content']
            )
            announced_ltv = string_utilis.string_to_float(
                dict_utils.DictUtil.find_dict_by_value_regex(mortgage_value_info, r"고시담보")['content']
            )
            expected_recovered_amount = string_utilis.korean_string_to_int(
                dict_utils.DictUtil.find_dict_by_value_regex(mortgage_value_info, r"담보물 회수 예상가액")['content']
            )
            mortgage_value = string_utilis.korean_string_to_int(
                dict_utils.DictUtil.find_dict_by_value_regex(mortgage_value_info, r"감정가")['content']
            )
            mtv = string_utilis.korean_string_to_int(
                dict_utils.DictUtil.find_dict_by_value_regex(mortgage_value_info, r"채권최고액 기준 담보비율")['content']
            )
            priority_amount = string_utilis.korean_string_to_int(
                dict_utils.DictUtil.find_dict_by_value_regex(mortgage_value_info, r"선순위 대출잔액")['content']
            )
            exclusive_area = string_utilis.string_to_float(
                dict_utils.DictUtil.find_dict_by_value_regex(mortgage_info, r"전용면적")['content']
            )
            floor_level = dict_utils.DictUtil.find_dict_by_value_regex(mortgage_info, r"층수")['content']
            converted_data.update({
                "expected_recovered_amount": expected_recovered_amount,
                "ltv": ltv,
                "mtv": mtv,
                "announced_ltv": announced_ltv,
                "mortgage_address": mortgage_address,
                "exclusive_area": exclusive_area,
                "floor_level": floor_level,
                "mortgage_value": mortgage_value,
                "priority_amount": priority_amount,
            })
        upsert_condition = Q(link=converted_data["link"])
        _ = FixedIncomeProduct.objects(upsert_condition).update_one(
            upsert=True, **converted_data
        )
        fip = FixedIncomeProduct.objects.get(upsert_condition)
        cls.upsert_expected_payments(fixed_income_id=fip.id)
        return fip
