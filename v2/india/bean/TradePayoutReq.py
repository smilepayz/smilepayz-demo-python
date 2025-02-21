from bean.TradeReq import TradeReq


class TradePayoutReq(TradeReq):
    def __init__(self, paymentMethod, payer, receiver, cashAccount, ifsccode,orderNo, purpose, productDetail, additionalParam,
                 itemDetailList, billingAddress, shippingAddress, money, merchant, callbackUrl, redirectUrl,area):
        super().__init__(orderNo, purpose, productDetail, additionalParam, itemDetailList, billingAddress,
                         shippingAddress, money, merchant, callbackUrl, redirectUrl,area)
        if paymentMethod is not None:
            self.paymentMethod = paymentMethod
        if payer is not None:
            self.payer = payer
        if receiver is not None:
            self.receiver = receiver
        if cashAccount is not None:
            self.cashAccount = cashAccount
        if ifsccode is not None:
            self.ifsccode = ifsccode