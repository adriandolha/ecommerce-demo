class Product:
    def __init__(self, product_id, name, category, price):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price

    def to_json(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'category': self.category,
            'price': self.price
        }
