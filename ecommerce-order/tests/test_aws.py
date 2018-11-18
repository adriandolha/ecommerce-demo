import json

import boto3

import aws
from ecommerce_order.serializers import to_json, from_json


class TestOrderApi:
    def test_order_list(self, order_valid):
        boto3.resource('dynamodb').Table('orders').scan.return_value = {'Items': [order_valid]}
        response = aws.list({})
        orders = json.loads(response['body'])
        assert 1 == len(orders)
        assert '200' == response['statusCode']

    def test_order_add(self, order_valid):
        response = aws.add({'body': to_json(order_valid)})
        assert '1' in from_json(response['body'])['user_id']
        assert '200' == response['statusCode']

    def test_order_created(self, order_valid):
        response = aws.order_created({'body': to_json(order_valid)})
        assert '200' == response['statusCode']
