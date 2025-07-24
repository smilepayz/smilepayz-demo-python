class MerchantReq:
    def __init__(self, merchantId, merchantName, accountNo,subMerchantId):
        if merchantId is not None:
            self.merchantId = merchantId
        if merchantName is not None:
            self.merchantName = merchantName
        if accountNo is not None:
            self.accountNo = accountNo
        if subMerchantId is not None:
            self.subMerchantId = subMerchantId

    def print_info(self):
        print(f"{self.merchantId} {self.merchantName} {self.accountNo}")