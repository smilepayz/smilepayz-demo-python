class PayerReq:
    def __init__(self, name, email, phone, pixAccount):
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
        if pixAccount is not None:
            self.pixAccount = pixAccount

    def print_info(self):
        print(f"{self.name} {self.email} {self.phone} {self.pixAccount} ")
