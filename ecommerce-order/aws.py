import uuid

from ecommerce_order.api import OrderApi


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
    return response(OrderApi(api_context(event, context)).order_created())
