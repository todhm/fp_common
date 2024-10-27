from typing import List, Tuple
from datetime import datetime, date
from scipy.optimize import newton

from dateutil.relativedelta import relativedelta

from fp_common.consts import TAX_RATE
from fp_common.models.fixed_income.fixed_income import ExpectedPayment, FixedIncomeProduct, PurchaseHistory


class ExpectedPaymentService(object):

    @classmethod
    def compute_expected_real_interest_rate(cls, fixed_income_product: FixedIncomeProduct):
        cash_flows = []
        investment_date = fixed_income_product.open_date.date()
        cash_flows.append((investment_date, -fixed_income_product.expected_invest_amount))

        for payment in fixed_income_product.expected_payments:
            payment_date = payment.payment_date.date()
            amount = payment.expected_amount
            cash_flows.append((payment_date, amount))
        rate = cls.xirr(cash_flows)
        if rate is not None:
            fixed_income_product.expected_real_interest_rate = rate * 100  # Convert to percentage
        else:
            fixed_income_product.expected_real_interest_rate = None

    @classmethod
    def xirr(cls, cash_flows: List[Tuple[date, int]]) -> float:
        """Compute the IRR for irregular cash flows."""
        dates = [cf[0] for cf in cash_flows]
        amounts = [cf[1] for cf in cash_flows]
        d0 = dates[0]
        times = [(d - d0).days / 365.0 for d in dates]

        def npv(rate):
            return sum([amt / (1 + rate) ** t for amt, t in zip(amounts, times)])

        try:
            result = newton(npv, 0.1)
            return result
        except (RuntimeError, OverflowError):
            return None

    @classmethod
    def upsert_expected_payments_with_product(
        cls,
        fixed_income_product: FixedIncomeProduct,
    ) -> List[ExpectedPayment]:
        payments = []
        monthly_interest_rate = fixed_income_product.interest_rate / 12 / 100  # Convert to decimal and monthly rate
        monthly_interest = fixed_income_product.expected_invest_amount * monthly_interest_rate
        start_date = fixed_income_product.start_date
        for month in range(1, fixed_income_product.term_value + 1):
            payment_date = start_date + relativedelta(months=+month)
            interest_amount = monthly_interest
            principal_repayment = 0
            total_payment = interest_amount + principal_repayment
            platform_fee = interest_amount * fixed_income_product.platform_fee_rate * 0.01
            tax_fee = interest_amount * TAX_RATE * 0.01
            expected_amount = total_payment - platform_fee - tax_fee

            # Round values to the nearest integer (assuming currency in won)
            expected_payment = ExpectedPayment(
                payment_date=payment_date,
                expected_amount=round(expected_amount),
                total_payment=int(round(total_payment)),
                platform_fee=int(round(platform_fee)),
                tax_fee=int(round(tax_fee))
            )
            payments.append(expected_payment)
        final_date = start_date + relativedelta(months=fixed_income_product.term_value)
        payments.append(ExpectedPayment(
            payment_date=final_date,
            expected_amount=fixed_income_product.expected_invest_amount,
            total_payment=fixed_income_product.expected_invest_amount,
            platform_fee=0,
            tax_fee=0
        ))
        fixed_income_product.expected_payments = payments
        cls.compute_expected_real_interest_rate(fixed_income_product)
        fixed_income_product.save()
        return payments

    @classmethod
    def upsert_expected_payments(
        self,
        purchase_history: PurchaseHistory,
    ) -> List[ExpectedPayment]:
        payments = []
        today = datetime.now()
        fixed_income_product: FixedIncomeProduct = purchase_history.product
        monthly_interest_rate = fixed_income_product.interest_rate / 12 / 100  # Convert to decimal and monthly rate
        monthly_interest = purchase_history.amount * monthly_interest_rate

        for month in range(1, fixed_income_product.term_value + 1):
            payment_date = today + relativedelta(months=+month)
            interest_amount = monthly_interest
            principal_repayment = 0
            total_payment = interest_amount + principal_repayment
            platform_fee = interest_amount * fixed_income_product.platform_fee_rate * 0.01
            tax_fee = interest_amount * TAX_RATE * 0.01
            expected_amount = total_payment - platform_fee - tax_fee

            # Round values to the nearest integer (assuming currency in won)
            expected_payment = ExpectedPayment(
                payment_date=payment_date,
                expected_amount=round(expected_amount),
                total_payment=int(round(total_payment)),
                platform_fee=int(round(platform_fee)),
                tax_fee=int(round(tax_fee))
            )
            payments.append(expected_payment)
        final_date = today + relativedelta(months=fixed_income_product.term_value)
        payments.append(ExpectedPayment(
            payment_date=final_date,
            expected_amount=purchase_history.amount,
            total_payment=purchase_history.amount,
            platform_fee=0,
            tax_fee=0
        ))
        purchase_history.expected_payments = payments
        purchase_history.save()
        return payments
