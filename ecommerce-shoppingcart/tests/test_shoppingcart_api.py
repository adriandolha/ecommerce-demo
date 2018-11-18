import json

import boto3

from ecommerce_shoppingcart.api import ShoppingCartApi
from ecommerce_shoppingcart.serializers import to_json


class TestShoppingCartApi:
    def test_shoppingcart_list(self, shoppingcart_valid):
        boto3.resource('dynamodb').Table('shoppingcarts').scan.return_value = {'Items': [shoppingcart_valid]}
        response = ShoppingCartApi({}).list()
        shoppingcarts = json.loads(response['body'])
        assert 1 == len(shoppingcarts)
        assert "1" == shoppingcarts[0]['user_id']
        assert '200' == response['status_code']

    def test_shoppingcart_add(self, shoppingcart_valid):
        response = ShoppingCartApi({'body': to_json(shoppingcart_valid)}).add()
        args_list = boto3.resource('dynamodb').Table('shoppingcarts').put_item.call_args_list
        args, kwargs = args_list[0]
        shoppingcart = json.loads(response['body'])
        print(shoppingcart)
        assert "1" == kwargs['Item']['user_id']
        assert "1" == shoppingcart['user_id']
        assert '200' == response['status_code']
