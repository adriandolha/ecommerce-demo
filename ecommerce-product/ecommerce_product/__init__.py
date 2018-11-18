import uuid

from ecommerce_product.domain import Product


def make_product(**kwargs):
    if not kwargs.get('product_id'):
        kwargs['product_id'] = str(uuid.uuid4())

    return Product(**kwargs)
