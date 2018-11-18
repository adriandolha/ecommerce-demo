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

    def test_order_created(self, order_created_event):
        args_list = boto3.resource('dynamodb').Table('orders').put_item.call_args_list
        aws.order_created(order_created_event)
        args, kwargs = args_list[0]
        assert "1" == kwargs['Item']['user_id']
        assert 320 == kwargs['Item']['total']
        assert 320 == kwargs['Item']['items'][0]['total']
