from fp_common.repositories.fixed_income.purchase_history import PurchaseHistoryRepository
from fp_common.services.fixed_income.expected_payment_services import ExpectedPaymentService
from fp_common.models.fixed_income.fixed_income import PurchaseHistory


class PurchaseHistoryService(object):

    @classmethod
    def upsert_expected_payments(
        self,
        purchase_history_id: str,
    ) -> PurchaseHistory:
        purchase_history = PurchaseHistoryRepository.find_by_id(purchase_history_id=purchase_history_id)
        ExpectedPaymentService.upsert_expected_payments(
            purchase_history=purchase_history,
        )
