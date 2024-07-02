
class BalanceInquiryReq:

    def __init__(self, partnerReferenceNo, accountNo,balanceTypes):
        if partnerReferenceNo is not None:
            self.partnerReferenceNo = partnerReferenceNo
        if accountNo is not None:
            self.accountNo = accountNo
        if balanceTypes is not None:
            self.balanceTypes = balanceTypes


    def print_info(self):
        print(f"{self.partnerReferenceNo} {self.accountNo} {self.balanceTypes}")