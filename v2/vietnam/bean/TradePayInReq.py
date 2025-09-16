from v2.vietnam.bean.TradeReq import TradeReq


class TradePayInReq(TradeReq):
    def __init__(self, paymentMethod, payer, expiryPeriod, orderNo, purpose,  money, merchant, callbackUrl, redirectUrl):
        super().__init__(orderNo, purpose , money, merchant, paymentMethod,callbackUrl)
        if paymentMethod is not None:
            self.paymentMethod = paymentMethod
        if payer is not None:
            self.payer = payer
        if expiryPeriod is not None:
            self.expiryPeriod = expiryPeriod
        if redirectUrl is not None:
            self.redirectUrl = redirectUrl
