import json

import boto3

import aws
from ecommerce_shoppingcart.api import ShoppingCartApi


class TestShoppingCartApi:
    def test_shoppingcart_list(self, shoppingcart_valid):
        boto3.resource('dynamodb').Table('shoppingcarts').scan.return_value = {'Items': [shoppingcart_valid]}
        response = aws.list({})
        shoppingcarts = json.loads(response['body'])
        assert 1 == len(shoppingcarts)
        assert '200' == response['statusCode']
