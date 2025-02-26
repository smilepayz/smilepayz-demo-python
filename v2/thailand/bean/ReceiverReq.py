class ReceiverReq:
    def __init__(self, name, email, phone):
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone

    def print_info(self):
        print(f"{self.name} {self.email} {self.phone}")
