class TradeReq:
    def __init__(self, orderNo, purpose, productDetail, additionalParam, itemDetailList, billingAddress,
                 shippingAddress, money, merchant, callbackUrl, redirectUrl):
        if orderNo is not None:
            self.orderNo = orderNo
        if purpose is not None:
            self.purpose = purpose
        if productDetail is not None:
            self.productDetail = productDetail
        if additionalParam is not None:
            self.additionalParam = additionalParam
        if itemDetailList is not None:
            self.itemDetailList = itemDetailList
        if billingAddress is not None:
            self.billingAddress = billingAddress
        if shippingAddress is not None:
            self.shippingAddress = shippingAddress
        if money is not None:
            self.money = money
        if merchant is not None:
            self.merchant = merchant
        if callbackUrl is not None:
            self.callbackUrl = callbackUrl
        if redirectUrl is not None:
            self.redirectUrl = redirectUrl
