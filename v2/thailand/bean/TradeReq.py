class TradeReq:
    def __init__(self, orderNo, purpose, money, merchant, callbackUrl, redirectUrl):
        if orderNo is not None:
            self.orderNo = orderNo
        if purpose is not None:
            self.purpose = purpose
        if money is not None:
            self.money = money
        if merchant is not None:
            self.merchant = merchant
        if callbackUrl is not None:
            self.callbackUrl = callbackUrl
        if redirectUrl is not None:
            self.redirectUrl = redirectUrl
