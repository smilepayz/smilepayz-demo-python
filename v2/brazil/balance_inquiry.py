import json

import requests

from v2.brazil import Tool_Sign
from v2.brazil.bean.BalanceInquiryReq import BalanceInquiryReq
from v2.brazil.bean.Constants import Constants


def balance_inquiry(env, merchant_id, merchant_secret, account_no, privateKey):
    global request_path
    print("=====> balance_inquiry")
    if env == "sandbox":
        request_path = Constants.baseUrlSandbox + "/v2.0/inquiry-balance"
    if env == "production":
        # production
        request_path = Constants.baseUrl + "/v2.0/inquiry-balance"

    # transaction time
    timestamp = Tool_Sign.get_formatted_datetime('Asia/Bangkok')
    print("timestamp:" + timestamp)

    # payInReq,  None fields are optional
    balance_inquiry_req = BalanceInquiryReq(account_no, ["BALANCE"])

    # jsonStr by json then minify
    json_data_minify = json.dumps(balance_inquiry_req, default=lambda o: o.__dict__, separators=(',', ':'))
    print("json_data_minify=", json_data_minify)

    # build
    string_to_sign = timestamp + "|" + merchant_secret + "|" + json_data_minify
    print("string_to_sign=", string_to_sign)
    print("request_path=", request_path)

    # signature
    signature = Tool_Sign.sha256RsaSignature(privateKey, string_to_sign)
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
balance_inquiry("sandbox", "", "", "", "")
