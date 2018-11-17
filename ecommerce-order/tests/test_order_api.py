import json

import boto3

from ecommerce_order.api import OrderApi
from ecommerce_order.serializers import to_json


class TestOrderApi:
    def test_order_list(self, order_valid):
        boto3.resource('dynamodb').Table('orders').scan.return_value = {'Items': [order_valid]}
        response = OrderApi({}).list()
        orders = json.loads(response['body'])
        assert 1 == len(orders)
        assert "1" == orders[0]['user_id']
        assert '200' == response['status_code']

    def test_order_add(self, order_valid):
        response = OrderApi({'body': to_json(order_valid)}).add()
        args_list = boto3.resource('dynamodb').Table('orders').put_item.call_args_list
        args, kwargs = args_list[0]
        order = json.loads(response['body'])
        print(order)
        assert "1" == kwargs['Item']['user_id']
        assert "1" == order['user_id']
        assert '200' == response['status_code']
