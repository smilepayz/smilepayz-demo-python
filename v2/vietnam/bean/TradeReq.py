class TradeReq:
    def __init__(self, orderNo, purpose, money, merchant,paymentMethod, callbackUrl):
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
        if paymentMethod is not None:
            self.paymentMethod = paymentMethod