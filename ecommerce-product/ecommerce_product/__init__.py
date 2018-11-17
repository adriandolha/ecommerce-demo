from ecommerce_product.domain import Product


def make_product(**kwargs):
    return Product(**kwargs)
