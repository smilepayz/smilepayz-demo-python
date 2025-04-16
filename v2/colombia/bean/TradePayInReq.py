from bean.TradeReq import TradeReq


class TradePayInReq(TradeReq):
    def __init__(self, paymentMethod, payer, receiver, expiryPeriod, orderNo, purpose, productDetail, additionalParam,
                 itemDetailList, billingAddress, shippingAddress, money, merchant, callbackUrl, redirectUrl,area):
        super().__init__(orderNo, purpose, productDetail, additionalParam, itemDetailList, billingAddress,
                         shippingAddress, money, merchant, callbackUrl, redirectUrl,area)
        if paymentMethod is not None:
            self.paymentMethod = paymentMethod
        if payer is not None:
            self.payer = payer
        if receiver is not None:
            self.receiver = receiver
        if expiryPeriod is not None:
            self.expiryPeriod = expiryPeriod