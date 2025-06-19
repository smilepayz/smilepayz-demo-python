class OrderStatusInquiry:

    def __init__(self, tradeType, tradeNo, orderNo):
        if tradeType is not None:
            self.tradeType = tradeType
        if tradeNo is not None:
            self.tradeNo = tradeNo
        if orderNo is not None:
            self.orderNo = orderNo

    def print_info(self):
        print(f"{self.tradeType} {self.tradeNo} {self.orderNo}")
