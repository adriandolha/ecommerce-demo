class ShoppingCart:
    def __init__(self, items, user_id=1):
        self.user_id = user_id
        self.items = items

    def to_json(self):
        return {
            'user_id':self.user_id,
            'items': self.items,
        }
