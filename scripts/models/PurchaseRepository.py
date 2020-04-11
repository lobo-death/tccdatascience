from scripts.models.models import Purchase, Items


class PurchaseRepository:

    @staticmethod
    def find_by_id(id):
        return Purchase.get(Purchase.id == id)

    @staticmethod
    def create(purchase):
        return Purchase.insert(purchase).execute()

    @staticmethod
    def insert_itens(item):
        Items.insert(item).execute()

    @staticmethod
    def get_purchase(id):
        return Purchase.select().join(Items).where(Purchase.id == id)
