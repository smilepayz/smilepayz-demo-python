import json

import requests

from v2.india import Tool_Sign
from v2.india.bean.AreaEnum import AreaEnum
from v2.india.bean.AreaEnum import CurrencyEnum
from v2.india.bean.Constants import Constants
from v2.india.bean.MerchantReq import MerchantReq
from v2.india.bean.MoneyReq import MoneyReq
from v2.india.bean.PayerReq import PayerReq
from v2.india.bean.TradePayInReq import TradePayInReq


def transaction_pay_in(env, merchant_id, merchant_secret, private_key, payment_method, amount, email):
    global request_path
    print("=====> PayIn transaction")
    if env == "sandbox":
        # sandbox
        request_path = Constants.baseUrlSandbox + "/v2.0/transaction/pay-in"
    if env == "production":
        # production
        request_path = Constants.baseUrl + "/v2.0/transaction/pay-in"

    # transaction time
    timestamp = Tool_Sign.get_formatted_datetime('Asia/Bangkok')
    print("timestamp:" + timestamp)

    # merchant_id
    merchant_order_no = merchant_id + Tool_Sign.generate_32bit_uuid()
    purpose = "Purpose For Transaction from python SDK"

    # demo for INDONESIA, replace CurrencyEnum,payment_method to you what need
    # moneyReq
    money_req = MoneyReq(CurrencyEnum.INR.name, amount)

    payer_req = PayerReq(None, email, None)

    # merchantReq
    merchant_req = MerchantReq(merchant_id, "", None)

    pay_in_req = TradePayInReq(payment_method, payer_req, None, None, merchant_order_no[:32], purpose,
                               None,
                               None,
                               None, None, None, money_req, merchant_req, "your notify url",
                               "redirect utl", AreaEnum.INDIA.code)

    # jsonStr by json then minify
    json_data_minify = json.dumps(pay_in_req, default=lambda o: o.__dict__, separators=(',', ':'))
    print("json_data_minify=", json_data_minify)

    # build
    string_to_sign = timestamp + "|" + merchant_secret + "|" + json_data_minify
    print("string_to_sign=", string_to_sign)
    print("request_path=", request_path)

    # signature
    signature = Tool_Sign.sha256RsaSignature(private_key, string_to_sign)
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
env = ""
merchant_id = ""
merchant_secret = ""
private_key = ""
payment_method = ""
amount = 100
email = ""
transaction_pay_in(env, merchant_id, merchant_secret, private_key, payment_method, amount, email)
