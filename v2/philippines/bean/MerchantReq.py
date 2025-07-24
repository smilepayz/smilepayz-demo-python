class MerchantReq:
    def __init__(self, merchantId, merchantName, accountNo):
        if merchantId is not None:
            self.merchantId = merchantId
        if merchantName is not None:
            self.merchantName = merchantName
        if accountNo is not None:
            self.accountNo = accountNo
            #如下是子商户
        # if subMerchantId is not None:
            # self.subMerchantId = subMerchantId

    def print_info(self):
        print(f"{self.merchantId} {self.merchantName} {self.accountNo}")