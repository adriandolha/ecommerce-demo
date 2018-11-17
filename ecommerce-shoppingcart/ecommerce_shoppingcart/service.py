from ecommerce_product.repo import ProductRepo


class ProductService:
    def __init__(self):
        self.repo = ProductRepo()

    def list(self):
        return self.repo.list()

    def add(self, product):
        self.repo.save(product)
