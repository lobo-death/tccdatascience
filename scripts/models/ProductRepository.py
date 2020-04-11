from scripts.models.models import Product


class ProductRepository:

    @staticmethod
    def find_by_id(id):
        return Product.get(Product.id == id)
