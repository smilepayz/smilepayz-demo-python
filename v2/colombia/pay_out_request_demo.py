import json

import requests

from v2.colombia import Tool_Sign
from v2.colombia.bean.CurrencyEnum import CurrencyEnum
from v2.colombia.bean.Constants import Constants
from v2.colombia.bean.MerchantReq import MerchantReq
from v2.colombia.bean.MoneyReq import MoneyReq
from v2.colombia.bean.TradePayoutReq import TradePayoutReq
from v2.colombia.bean.ReceiverReq import ReceiverReq


def pay_out_request_demo(env, merchant_id, merchant_secret, private_key,
                         payment_method, amount, cash_account,cash_account_type,receiver_req):
    global request_path
    if env == "production":
        # production
        request_path = Constants.baseUrl + "/v2.0/disbursement/pay-out"
    if env == "sandbox":
        # sandbox
        request_path = Constants.baseUrlSandbox + "/v2.0/disbursement/pay-out"

    # transaction time
    timestamp = Tool_Sign.get_formatted_datetime('America/Lima')
    print("timestamp:" + timestamp)
    # partner_id
    merchant_order_no = merchant_id + Tool_Sign.generate_32bit_uuid()
    purpose = "Purpose For Transaction from python SDK"

    # moneyReq
    money_req = MoneyReq(CurrencyEnum.COP.name, amount)
    # merchantReq
    merchant_req = MerchantReq(merchant_id, "your merchant name", None)


    # payInReq
    pay_in_req = TradePayoutReq(payment_method, None, receiver_req, cash_account,cash_account_type,
                                merchant_order_no[:32], purpose,
                                None,
                                None,
                                None, None, None, money_req, merchant_req, "notify url",
                                None )

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
    print("response result=", result)


# run
if __name__ == '__main__':

    env = ""
    merchant_id = ""
    merchant_secret = ""
    private_key = ""
    payment_method = ""
    amount = 100
    cash_account = ""
    cash_account_type = ""
    receiver_req = ReceiverReq("receiver", "email", "123232323","1232323232","CC")
    pay_out_request_demo(env, merchant_id, merchant_secret, private_key, payment_method, amount, cash_account,
                         cash_account_type,receiver_req)
