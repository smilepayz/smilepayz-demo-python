import json

import requests

from v2.indonesia import Tool_Sign
from v2.indonesia.bean.OrderStatusInquiry import OrderStatusInquiry
from v2.indonesia.bean.Constants import Constants


def status_inquiry(env,merchant_id,merchant_secret,private_key,trade_type,trade_no,order_no,):
    global  request_path
    if env == "production":
        # production
        request_path = Constants.baseUrl + "/v2.0/inquiry-status"

    if env == "sandbox":
        # sandbox
        request_path = Constants.baseUrlSandbox + "/v2.0/inquiry-status"

    # transaction time
    timestamp = Tool_Sign.get_formatted_datetime('Asia/Bangkok')
    print("timestamp:" + timestamp)

    # payInReq,  None fields are optional
    order_status_inquiry = OrderStatusInquiry(trade_type, trade_no,order_no)

    # jsonStr by json then minify
    json_data_minify = json.dumps(order_status_inquiry, default=lambda o: o.__dict__, separators=(',', ':'))
    print("json_data_minify=", json_data_minify)

    # build
    string_to_sign = timestamp + "|" + merchant_secret + "|" + json_data_minify
    print("string_to_sign=", string_to_sign)

    # signature
    signature = Tool_Sign.sha256RsaSignature(private_key, string_to_sign)
    print("signature=", signature)
    print("request_path=", request_path)

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
env = ""
merchant_id = ""
merchant_secret = ""
private_key = ""
trade_type = ""
trade_no = ""
order_no = ""
status_inquiry(env,merchant_id,merchant_secret,private_key,trade_type,trade_no,order_no)
