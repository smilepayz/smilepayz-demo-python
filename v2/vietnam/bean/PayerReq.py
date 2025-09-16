class PayerReq:
    def __init__(self, name, email, phone, accountNo, bankName):
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
        if accountNo is not None:
            self.accountNo = accountNo
        if bankName is not None:
            self.bankName = bankName

    def print_info(self):
        print(f"{self.name} {self.email} {self.phone} {self.accountNo}{self.bankName} ")
