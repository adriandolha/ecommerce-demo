from ecommerce_product import make_product
from ecommerce_product.serializers import to_json, from_json
from ecommerce_product.service import ProductService


class ProductApi:
    def __init__(self, context):
        self.context = context

    def list(self):
        return to_json([product.to_json() for product in ProductService().list()])

    def add(self, product):
        return ProductService().add(make_product(**product))
