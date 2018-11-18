from functools import wraps

from ecommerce_order import make_order
from ecommerce_order.serializers import to_json, from_json
from ecommerce_order.service import OrderService


def response(message, status_code):
    return {
        'status_code': str(status_code),
        'body': to_json(message)
    }


def handle_request():
    """
    Handle common exceptions.
    :return: Decorated function.
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return response(f(*args, *kwargs), 200)
            except ValueError as e:
                return response(str(e), 412)
            except KeyError as e:
                return response(str(e), 412)

        return wrapper

    return decorator


class OrderApi:
    def __init__(self, context):
        self.context = context

    @handle_request()
    def list(self):
        return [order.to_json() for order in OrderService().list()]

    @handle_request()
    def add(self):
        order = from_json(self.context['body'])
        print(f'Saving order {order}')
        return OrderService().add(make_order(**order))

    @handle_request()
    def order_created(self):
        order = from_json(self.context['body'])
        print(f'Order created {order}')
        return 'ok'  # OrderService().update(make_order(**order))
