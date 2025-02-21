class MoneyReq:
    def __init__(self, currency, amount):
        if currency is not None:
            self.currency = currency
        if amount is not None:
            self.amount = amount

    def print_info(self):
        print(f"{self.currency} {self.amount}")