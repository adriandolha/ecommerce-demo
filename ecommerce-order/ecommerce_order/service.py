from ecommerce_order.repo import OrderRepo


class OrderService:
    def __init__(self):
        self.repo = OrderRepo()

    def list(self):
        return self.repo.list()

    def add(self, order):
        self.repo.save(order)
        return order.to_json()
