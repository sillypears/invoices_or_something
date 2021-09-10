class Order(object):
    def __init__(self, item, entity, first, email, price, shipping) -> None:
        self.item = item
        self.entity = entity
        self.first_name = first
        self.last_name = ""
        self.email = email
        self.price = price
        self.shipping = shipping
        