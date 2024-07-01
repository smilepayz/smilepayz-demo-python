class PayerReq:
    def __init__(self, name, email, phone, address, identity):
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
        if address is not None:
            self.address = address
        if identity is not None:
            self.identity = identity

    def print_info(self):
        print(f"{self.name} {self.email} {self.phone} {self.address} {self.identity}")