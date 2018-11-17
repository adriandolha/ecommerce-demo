from ecommerce_order.domain import Order


def make_order(**kwargs):
    return Order(**kwargs)
