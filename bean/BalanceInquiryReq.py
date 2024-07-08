
class BalanceInquiryReq:

    def __init__(self, accountNo,balanceTypes):
        if accountNo is not None:
            self.accountNo = accountNo
        if balanceTypes is not None:
            self.balanceTypes = balanceTypes


    def print_info(self):
        print(f" {self.accountNo} {self.balanceTypes}")