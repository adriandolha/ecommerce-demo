import uuid

import boto3

from ecommerce_shoppingcart import make_shoppingcart
from ecommerce_shoppingcart.domain import ShoppingCart


class ShoppingCartRepo:
    def __init__(self):
        self.ddb = boto3.resource('dynamodb')
        self.table_name = 'shoppingcarts'
        self.table = self.ddb.Table(self.table_name)

    def save(self, shoppingcart: ShoppingCart):
        print(f'Saving shoppingcart {shoppingcart.to_json()}')
        if not shoppingcart.shoppingcart_id:
            shoppingcart.shoppingcart_id = str(uuid.uuid4())
        self.table.put_item(Item=shoppingcart.to_json())

    def list(self):
        return [make_shoppingcart(**item) for item in self.table.scan()['Items']]
