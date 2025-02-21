import json

import requests

from v2.brazil import Tool_Sign
from v2.brazil.bean.AreaEnum import AreaEnum
from v2.brazil.bean.AreaEnum import CurrencyEnum
from v2.brazil.bean.Constants import Constants
from v2.brazil.bean.MerchantReq import MerchantReq
from v2.brazil.bean.MoneyReq import MoneyReq
from v2.brazil.bean.PayerReq import PayerReq
from v2.brazil.bean.TradePayInReq import TradePayInReq


def transaction_pay_in(env="sandbox"):
    global merchant_id, merchant_secret, request_path
    print("=====> PayIn transaction")
    if env == "sandbox":
         # sandbox
        merchant_id = Constants.merchantIdSandBox
        merchant_secret = Constants.merchantSecretSandBox
        request_path = Constants.baseUrlSandbox + "/v2.0/transaction/pay-in"
    if env == "production":
        # production
        merchant_id = Constants.merchantId
        merchant_secret = Constants.merchantSecret
        request_path = Constants.baseUrl + "/v2.0/transaction/pay-in"

    # transaction time
    timestamp = Tool_Sign.get_formatted_datetime('Asia/Bangkok')
    print("timestamp:" + timestamp)

    # partner_id
    merchant_order_no = merchant_id + Tool_Sign.generate_32bit_uuid()
    purpose = "Purpose For Transaction from python SDK"

    # demo for INDONESIA, replace CurrencyEnum,payment_method to you what need
    payment_method = "PIX"
    # moneyReq
    money_req = MoneyReq(CurrencyEnum.BRL.name, 10000)

    # merchantReq
    merchant_req = MerchantReq(merchant_id, "your merchant name", None)

    # payerReq
    payer_req = PayerReq(None, None, None,"12345678900")

    pay_in_req = TradePayInReq(payment_method, payer_req, None, None, merchant_order_no[:32], purpose,
                               None,
                               None,
                               None, None, None, money_req, merchant_req, "your notify url",
                               "redirect utl", AreaEnum.BRAZIL.code)

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
    print("response result =", result)


# run
transaction_pay_in("production")
