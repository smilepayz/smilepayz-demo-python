class ReceiverReq:
    #For Peru: DNI：ID Card, CE：Foreigner ID card,PAS：Passport,RUC：Taxpayer registration number
    #For Colombia: CC : Domestic documents,CE：Foreigner documents

    def __init__(self, name, email, phone, identity, idType):
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
        if identity is not None:
            self.identity = identity
        if idType is not None:
            idtype = idType

    def print_info(self):
        print(f"{self.name} {self.email} {self.phone} ")
