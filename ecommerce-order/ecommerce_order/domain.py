class Order:
    def __init__(self, order_id, items, user_id="1", status="CREATED"):
        self.order_id = order_id
        self.status = status
        self.user_id = user_id
        self.items = items

    def to_json(self):
        return {
            'order_id': self.order_id,
            'user_id': self.user_id,
            'items': self.items,
            'status': self.status
        }
