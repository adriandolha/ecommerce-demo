import boto3
import pytest
from mock import mock


@pytest.fixture()
def product_valid(mock_ddb_table):
    yield {"product_id": "67689cbd-f560-4556-bf69-f630d58d00b1",
           "name": "Headset",
           "category": "Electronics",
           "price": 160
           }


@pytest.fixture(scope='session')
def mock_ddb_table():
    with mock.patch('boto3.resource'):
        yield boto3.resource('dynamodb').Table('products')
