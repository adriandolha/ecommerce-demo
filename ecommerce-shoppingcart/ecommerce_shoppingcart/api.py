import json
from functools import wraps

from ecommerce_shoppingcart import make_shoppingcart
from ecommerce_shoppingcart.serializers import to_json, from_json
from ecommerce_shoppingcart.service import ShoppingCartService


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


class ShoppingCartApi:
    def __init__(self, context):
        self.context = context

    @handle_request()
    def list(self):
        return [shoppingcart.to_json() for shoppingcart in ShoppingCartService().list()]

    @handle_request()
    def add(self, shoppingcart):
        return ShoppingCartService().add(make_shoppingcart(**shoppingcart))
