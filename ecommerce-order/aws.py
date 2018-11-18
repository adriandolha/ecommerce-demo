import uuid

from ecommerce_order.api import OrderApi
import logging
LOGGER = logging.getLogger('ecommerce')

def response(api_response):
    return {
        'statusCode': api_response['status_code'],
        'body': api_response['body']
    }


def api_context(event, context):
    if not event:
        event = {}
    if not context:
        context = {}
    return {
        'user_id': str(uuid.uuid4()),
        'body': event.get('body') or {},
        'path_parameters': event.get('pathParameters') or {}
    }


def list(event, context=None):
    print(event)
    print(context)
    return response(OrderApi(api_context(event, context)).list())


def add(event, context=None):
    print(event)
    print(context)
    return response(OrderApi(api_context(event, context)).add())


def order_created(event, context=None):
    print(event)
    print(context)
    try:
        OrderApi(order_created_context(event)).order_created()
    except KeyError as e:
        print('Error updating order.')
        LOGGER.error(e)


def order_created_context(event):
    if not event:
        return {}

    item = event['Records'][0]['dynamodb'].get('NewImage') or event['Records'][0]['dynamodb'].get('OldImage')
    return {
        'event_name': event['Records'][0]['eventName'],
        'order': {
            'user_id': item['user_id']['S'],
            'order_id': item['order_id']['S'],
            'items': [extract_item(order_item) for order_item in item['items']['L']],
        }
    }


def extract_item(order_item):
    """
    Excludes 'S' and 'M' keys, for one level
    Need to be improved, for parameters with map values
    :param order_item: dict
    :return: dict
    """
    print(f'Extracting order item from event item {order_item}')
    return {k: [val for key, val in enumerate(v.values())][0] for k, v in order_item['M'].items()}
