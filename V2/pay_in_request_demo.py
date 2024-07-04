import json
import time

import requests

import Tool_Sign
from bean.AddressReq import AddressReq
from bean.AreaEnum import AreaEnum
from bean.AreaEnum import CurrencyEnum
from bean.ItemDetailReq import ItemDetailReq
from bean.MerchantReq import MerchantReq
from bean.MoneyReq import MoneyReq
from bean.PayerReq import PayerReq
from bean.ReceiverReq import ReceiverReq
from bean.TradePayInReq import TradePayInReq
from bean.Constants import Constants


def transaction_pay_in():
    print("=====> PayIn transaction")

    # production
    merchant_id = Constants.merchantId
    merchant_secret = Constants.merchantSecret
    request_path = Constants.baseUrl + "/v2.0/transaction/pay-in"

    # sandbox
    # merchant_id = Constants.merchantIdSandBox
    # merchant_secret = Constants.merchantSecretSandBox
    # request_path = Constants.baseUrlSandbox + "/v2.0/transaction/pay-in"

    # transaction time
    timestamp = Tool_Sign.get_formatted_datetime('Asia/Bangkok')
    print("timestamp:" + timestamp)

    # partner_id
    merchant_order_no = merchant_id + Tool_Sign.generate_32bit_uuid()
    purpose = "Purpose For Transaction from python SDK"

    payment_method = "W_DANA"  #for indonesia
    # moneyReq
    money_req = MoneyReq(CurrencyEnum.IDR.name, 10000)
    # merchantReq
    merchant_req = MerchantReq(merchant_id, None, None)

    # payerReq optional
    payer_req = PayerReq("Jef-fer", "jef.gt@gmail.com", "82-3473829260",
                         "Jalan Pantai Mutiara TG6, Pluit, Jakarta", None)
    # receiverReq optional
    receiver_req = ReceiverReq("Viva in", "Viva@mir.com", "82-3473233732",
                               "Jl. Pluit Karang Ayu 1 No.B1 Pluit", None)
    # itemDetailReq optional
    item_detail_req = ItemDetailReq("mac A1", 1, 10000)
    item_detail_req_list = [item_detail_req]

    # billingAddress optional
    billing_address = AddressReq("Jl. Pluit Karang Ayu 1 No.B1 Pluit", "jakarta",
                                 "14450", "82-3473233732", "Indonesia")
    # shippingAddress optional
    shipping_address = AddressReq("Jl. Pluit Karang Ayu 1 No.B1 Pluit", "jakarta",
                                  "14450", "82-3473233732", "Indonesia")

    # payInReq,  None fields are optional
    pay_in_req = TradePayInReq(payment_method, None, None, None, merchant_order_no[:32], purpose,
                               None,
                               None,
                               None, None, None, money_req, merchant_req, None,
                               None, AreaEnum.INDONESIA.code)

    # jsonStr by json then minify
    json_data_minify = json.dumps(pay_in_req, default=lambda o: o.__dict__, separators=(',', ':'))
    print("json_data_minify=", json_data_minify)

    # build
    string_to_sign = timestamp + "|" + merchant_secret + "|" + json_data_minify
    print("string_to_sign=", string_to_sign)
    print("request_path=", request_path)

    # signature
    signature = Tool_Sign.sha256RsaSignature(Constants.privateKeyStr, string_to_sign)
    print("signature=", signature)

    # post
    # header
    headers = {
        'Content-Type': 'application/json',
        'X-TIMESTAMP': timestamp,
        'X-SIGNATURE': signature,
        'X-PARTNER-ID': merchant_id,

    }
    # POST request
    response = requests.post(request_path, data=json_data_minify, headers=headers)
    # Get response result
    result = response.json()
    print(result)


# run
transaction_pay_in()
