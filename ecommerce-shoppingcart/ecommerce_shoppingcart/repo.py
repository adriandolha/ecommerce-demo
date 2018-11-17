import uuid

import boto3

from ecommerce_product import make_product
from ecommerce_product.domain import Product


class ProductRepo:
    def __init__(self):
        self.ddb = boto3.resource('dynamodb')
        self.table_name = 'products'
        self.table = self.ddb.Table(self.table_name)

    def save(self, product: Product):
        print(f'Saving product {product.to_json()}')
        if not product.product_id:
            product.product_id = str(uuid.uuid4())
        self.table.put_item(Item=product.to_json())

    def list(self):
        return [make_product(**item) for item in self.table.scan()['Items']]
