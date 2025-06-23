class ItemDetailReq:
    def __init__(self, name, quantity, price):
        if name is not None:
            self.name = name
        if quantity is not None:
            self.quantity = quantity
        if price is not None:
            self.price = price

    def print_info(self):
        print(f"{self.name} {self.quantity} {self.price}")