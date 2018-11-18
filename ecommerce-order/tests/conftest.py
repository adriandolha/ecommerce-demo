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
            "count": 2,
            "category": "Electronics",
            "price": 160}]
    }


@pytest.fixture()
def order_created_event(mock_ddb_table):
    return {'Records': [{'eventID': '4273cd3777d3adf21f2e24108bb5fb29', 'eventName': 'INSERT', 'eventVersion': '1.1',
                         'eventSource': 'aws:dynamodb', 'awsRegion': 'us-east-1',
                         'dynamodb': {'ApproximateCreationDateTime': 1542533700.0, 'Keys': {'user_id': {'S': '1'},
                                                                                            'order_id': {
                                                                                                'S': '130fa9d4-41b1-46b0-a2f2-772cac2e6759'}},
                                      'NewImage': {'total': {'N': '320'}, 'user_id': {'S': '1'}, 'items': {'L': [{'M': {
                                          'total': {'N': '320'}, 'price': {'N': '160'},
                                          'product_id': {'S': '67689cbd-f560-4556-bf69-f630d58d00b1'},
                                          'name': {'S': 'Headset'}, 'count': {'N': '2'},
                                          'category': {'S': 'Electronics'}}}]},
                                                   'order_id': {'S': '130fa9d4-41b1-46b0-a2f2-772cac2e6759'},
                                                   'status': {'S': 'CREATED'}},
                                      'SequenceNumber': '2428900000000018730127725', 'SizeBytes': 242,
                                      'StreamViewType': 'NEW_AND_OLD_IMAGES'},
                         'eventSourceARN': 'arn:aws:dynamodb:us-east-1:103050589342:table/orders/stream/2018-11-17T19:50:57.948'}]}


@pytest.fixture()
def order_new(mock_ddb_table):
    yield {
        "user_id": "1",
        "items": [{
            "product_id": "67689cbd-f560-4556-bf69-f630d58d00b1",
            "name": "Headset",
            "category": "Electronics",
            "count": 2,
            "price": 160}]
    }


@pytest.fixture(scope='session')
def mock_ddb_table():
    with mock.patch('boto3.resource'):
        yield boto3.resource('dynamodb').Table('orders')
