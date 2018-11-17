import json
from functools import wraps

from ecommerce_product import make_product
from ecommerce_product.serializers import to_json, from_json
from ecommerce_product.service import ProductService


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


class ProductApi:
    def __init__(self, context):
        self.context = context

    @handle_request()
    def list(self):
        return [product.to_json() for product in ProductService().list()]

    @handle_request()
    def add(self, product):
        return ProductService().add(make_product(**product))
