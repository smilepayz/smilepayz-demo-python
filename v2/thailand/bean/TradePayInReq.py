from v2.thailand.bean.TradeReq import TradeReq


class TradePayInReq(TradeReq):
    def __init__(self, paymentMethod, payer, receiver, expiryPeriod, orderNo, purpose, money, merchant, callbackUrl, redirectUrl):
        super().__init__(orderNo, purpose, money, merchant, callbackUrl, redirectUrl)
        if paymentMethod is not None:
            self.paymentMethod = paymentMethod
        if payer is not None:
            self.payer = payer
        if receiver is not None:
            self.receiver = receiver
        if expiryPeriod is not None:
            self.expiryPeriod = expiryPeriod