import json

import boto3

import aws
from ecommerce_product.api import ProductApi


class TestProductApi:
    def test_product_list(self, product_valid):
        boto3.resource('dynamodb').Table('products').scan.return_value = {'Items': [product_valid]}
        response = aws.list({})
        products = json.loads(response['body'])
        assert 1 == len(products)
        assert '200' == response['statusCode']
