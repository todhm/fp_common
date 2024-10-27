from fp_common.models.fixed_income.fixed_income import FixedIncomeProduct


class FixedIncomeProductRepository(object):

    @classmethod
    def find_by_id(
        self,
        fixed_income_product_id: str
    ) -> FixedIncomeProduct:
        return FixedIncomeProduct.objects(id=fixed_income_product_id).first()
