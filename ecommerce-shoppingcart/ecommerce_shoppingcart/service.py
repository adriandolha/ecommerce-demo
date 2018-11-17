from ecommerce_shoppingcart.repo import ShoppingCartRepo


class ShoppingCartService:
    def __init__(self):
        self.repo = ShoppingCartRepo()

    def list(self):
        return self.repo.list()

    def add(self, shoppingcart):
        self.repo.save(shoppingcart)
