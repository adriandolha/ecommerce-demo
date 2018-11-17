import uuid

import boto3

from ecommerce_order import make_order
from ecommerce_order.domain import Order


class OrderRepo:
    def __init__(self):
        self.ddb = boto3.resource('dynamodb')
        self.table_name = 'orders'
        self.table = self.ddb.Table(self.table_name)

    def save(self, order: Order):
        print(f'Saving order {order.to_json()}')
        if not order.user_id:
            order.order_id = str(uuid.uuid4())
        self.table.put_item(Item=order.to_json())
        print(f'Saved order {order.to_json()}')

    def list(self):
        return [make_order(**item) for item in self.table.scan()['Items']]
