import boto3
import pytest
from mock import mock


@pytest.fixture()
def order_valid(mock_ddb_table):
    yield {
        "order_id": "0797bef1-5c57-4d9c-9c8d-3e1615b837bd",
        "user_id": "1",
        "items": [{
            "product_id": "67689cbd-f560-4556-bf69-f630d58d00b1",
            "name": "Headset",
            "category": "Electronics",
            "price": 160}]
    }


@pytest.fixture(scope='session')
def mock_ddb_table():
    with mock.patch('boto3.resource'):
        yield boto3.resource('dynamodb').Table('orders')
