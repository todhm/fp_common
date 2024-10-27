from fixed_income.models import PurchaseHistory


class PurchaseHistoryRepository(object):

    @classmethod
    def find_by_id(
        self,
        purchase_history_id: str
    ) -> PurchaseHistory:
        return PurchaseHistory.objects(id=purchase_history_id).first()