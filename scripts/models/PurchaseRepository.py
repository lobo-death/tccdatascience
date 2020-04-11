from scripts.models.models import Purchase, Items


class PurchaseRepository:

    @staticmethod
    def find_by_id(id):
        return Purchase.get(Purchase.id == id)

    @staticmethod
    def create(purchase):
        return Purchase.insert(purchase)

    @staticmethod
    def insert_itens(itens):
        for item in itens:
            Items.insert(item)

    @staticmethod
    def get_purchase(id):
        return Purchase.select().join(Items).where(Purchase.id == id)
