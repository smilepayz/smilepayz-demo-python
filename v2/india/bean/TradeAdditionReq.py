class TradeAdditionReq:
    # ifscode: Only for India Pay out to Bank ,11 digits (Mandatory)
    # taxNumber : Only for Brazil pay out , which method is CPF/CNPJ ,this is tax number for CPF/CNPJ
    # payerAccountNo : Only for Thailand pay in ,this is means your paying bank account no
    def __init__(self, ifscCode, taxNumber, payerAccountNo):
        if ifscCode is not None:
            self.ifscCode = ifscCode
        if taxNumber is not None:
            self.taxNumber = taxNumber
        if payerAccountNo is not None:
            self.payerAccountNo = payerAccountNo



    def print_info(self):
        print(f" {self.ifscCode} {self.taxNumber} {self.payerAccountNo}")