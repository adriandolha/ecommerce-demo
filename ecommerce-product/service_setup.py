import json

from ecommerce_product.api import ProductApi
if __name__=='__main__':
    product_api = ProductApi({})
    with open('products.json') as file:
        products_json = ''.join(file.readlines())
    for product in json.loads(products_json):
        product_api.add(product)
