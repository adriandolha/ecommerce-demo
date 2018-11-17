import json

import boto3

import aws
from ecommerce_shoppingcart.api import ShoppingCartApi
from ecommerce_shoppingcart.serializers import to_json, from_json


class TestShoppingCartApi:
    def test_shoppingcart_list(self, shoppingcart_valid):
        boto3.resource('dynamodb').Table('shoppingcarts').scan.return_value = {'Items': [shoppingcart_valid]}
        response = aws.list({})
        shoppingcarts = json.loads(response['body'])
        assert 1 == len(shoppingcarts)
        assert '200' == response['statusCode']

    def test_shoppingcart_add(self, shoppingcart_valid):
        response = aws.add({'body': to_json(shoppingcart_valid)})
        assert '1' in from_json(response['body'])['user_id']
        assert '200' == response['statusCode']
