class TradeAdditionReq:
    def __init__(self, ifscCode, taxNumber, payerAccountNo, network):
        if ifscCode is not None:
            self.ifscCode = ifscCode
        if taxNumber is not None:
            self.taxNumber = taxNumber
        if payerAccountNo is not None:
            self.payerAccountNo = payerAccountNo
        if network is not None:
            self.network = network


    def print_info(self):
        print(f" {self.ifscCode} {self.taxNumber} {self.payerAccountNo} {self.network}")