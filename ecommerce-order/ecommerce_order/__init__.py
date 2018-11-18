import uuid

from ecommerce_order.domain import Order


def make_order(**kwargs):
    if not kwargs.get('order_id'):
        kwargs['order_id'] = str(uuid.uuid4())
    return Order(**kwargs)
