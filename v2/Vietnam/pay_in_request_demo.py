import json

import requests

from v2.Vietnam import Tool_Sign
from v2.Vietnam.bean.AreaEnum import AreaEnum
from v2.Vietnam.bean.AreaEnum import CurrencyEnum
from v2.Vietnam.bean.Constants import Constants
from v2.Vietnam.bean.MerchantReq import MerchantReq
from v2.Vietnam.bean.MoneyReq import MoneyReq
from v2.Vietnam.bean.PayerReq import PayerReq
from v2.Vietnam.bean.TradePayInReq import TradePayInReq


def transaction_pay_in(env, merchant_id, merchant_secret, private_key, payment_method, amount, payer_name,
                       payer_account, payer_bank):
    global request_path
    print("=====> PayIn transaction")
    if env == "sandbox":
        # sandbox
        request_path = Constants.baseUrlSandbox + "/v2.0/transaction/pay-in"
    if env == "production":
        # production
        request_path = Constants.baseUrl + "/v2.0/transaction/pay-in"

    # transaction time
    # 时区越南胡志明市(Asia/Ho_Chi_Minh)
    timestamp = Tool_Sign.get_formatted_datetime('Asia/Ho_Chi_Minh')
    print("timestamp:" + timestamp)

    # partner_id
    merchant_order_no = merchant_id + Tool_Sign.generate_32bit_uuid()
    purpose = "Purpose For Transaction from python SDK"

    # moneyReq
    money_req = MoneyReq(CurrencyEnum.VND.name, amount)

    # merchantReq
    merchant_req = MerchantReq(merchant_id, "your merchant name", None)

    # payerReq
    payer_req = PayerReq(payer_name, None, None, payer_account, payer_bank)

    pay_in_req = TradePayInReq(payment_method, payer_req, None, None, merchant_order_no[:32], purpose,
                               None,
                               None,
                               None, None, None, money_req, merchant_req, "https://www.thb.com",
                               "https://www.vnd.com")

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
    # 断言
    assert result['code'] == '00', f"接口调用失败，code={result['code']},message={result.get('message')}"
    assert 'tradeNo' in result and result['tradeNo'], "tradeNo缺失或为空"
    assert 'orderNo' in result and result['orderNo'], "orderNo缺失或为空"
    assert 'status' in result, "返回结果缺少status字段"
    assert result['status'] in ['PROCESSING', 'SUCCESS','INIT'], f"状态异常：{result['status']}"
    assert 'money' in result, "返回结果缺少money字段"
    assert 'amount' in result['money'], "money字段缺少amount"
    assert abs(result['money']['amount'] - amount) < 0.01, f"金额不匹配，返回金额：{result['money']['amount']}，请求金额：{amount}"
    assert 'currency' in result['money'], "money字段缺少currency"
    assert result['money']['currency'] == 'VND', f"币种错误，返回币种：{result['money']['currency']}"
    assert 'channel' in result, "返回结果缺少channel字段"
    assert 'paymentMethod' in result['channel'], "channel字段缺少paymentMethod"
    assert result['channel']['paymentMethod'] == 'VIET_QR', f"支付方式不匹配，返回支付方式：{result['channel']['paymentMethod']}"

# run
if __name__ == '__main__':
    env = 'production'
    merchant_id = '20158'
    merchant_secret = 'ebef0a7119b5208e84633f63dafd61110ae97e24ee4d120bb04045aa28111671'
    private_key = 'MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDDUFDuFqO8Q9Dr0xmHTSNoWDG1nwX3rroX5oUdpUrP1jUTejyb4pQ6Yim9o4Fh1pbrHa1499d7tGgPycSq5uFzv9O+jkSSRbnUvM4nh+ktpvBwWPw6vTYP/8pZ88yzXzDdIO6bXN0XkcM44cCfmohkldIdg2DO+i8H15opilVqDCGFgi/peK/bOsN/Nw6VMHAacITBHfJhFqSSgJQgHCc+H1OTjN7TWmGkPBi8Alpzcl6ZWBFIMT35m5hy7OPY4In1/MnytyQG+wOYiVmSzxg5E2S9vooKANpybmLuBI0T32ZEpNevSUwySlFfFXB52QIDbaZKAy4Jc7wuNbc9o6WLAgMBAAECggEALpaLX2deEgu5G29kwP3Y6sxSuyheA4kVkZrmeL5TPIUzbtxy9ZoT0mNU4ovMUlqd8CJJnTe9GiBbzBxMQZnGAFaq+uKzn5JrM7//irVkHQQbiSjorVgxu5o/mbpKQyT7Ilv3Hm8Fu9gEkZ5j1I5HZ3rHPkv2vRg3PK8kcjExk5Q66tmwx4Trhy4UbwPVWcFkf10bHpkQPBBBtAwXqPMFnG0e91pE8EVrfvGECEDSSp/hqTKLzoeWsJcRJH0DdA8Z1WGtEXCrNOlFvm0b1s3ZBuoUS9fGCoysq3Fqz1b4dAmO19kIaUUIqkHAjNBmEftC3FbivL+RPXmWww94QbhkwQKBgQD4jyRvfr5IAbqa6Da5ltbJkIF73EAM+7gVYpeDJI2rW3Twj9yLzOcuHthdXum7cvJ/Kqn5a3SwEvNHTXgLozlKD+wUUM/dQIgVMZIgGGTWEDox8ifjJxsxo9bOt8hkNV3ENtpXpbcXSlgDW1/vWJNGU/dISI/MS8zH209bLFDdwQKBgQDJKR9OqjDL0wWnrOI11iSOEZNaa1Yh51rpSKAXQyAh3/OXAlNgc/WmMnw02HwOaOLpNz5RW44Zi6z2yCi0ZM653lPPwjfFXp/jsF/KPqOcRe5DS6YUgtbeP6SzRe9kRgL3LbfkghvM0IWUGnCevXAiMLDN4IeZLGHZ9K8iVJouSwKBgARy428PcK5vQXzGTTxzI7MF4BtsbMUOuFPBqP6S5+o6P9SSbpsd9sFPkgXRzhMp0odOJy6sqrEAFdSf4Vcr+7mEoXAXpjDKl+TxNzFV3nAqaDA+qlIZgBYaXZzjkzWf8uaxKKVK9QT4sqyUtRnelvw6QoHLsq8waCDnnvr9xxDBAoGBAJS6kcowrQlWSV0SxuG1JavgtMjqiXFhw+ataqgoWi6RjWF+N7Udp2cs9oZ/9SEWTYbO8IVoouSiT8zaarYNvobQKbl3SJLmBmNq+TfoHkGhtqsM2ItbvY/vEE/4CipiVTj6FXee9vz0w36gGdpUB/9PbrmZI8iNdv+WGJLSaHiHAoGBAKkTd+OzbkanMW8E/NLx7z+i98J4b83J5T6nf4UlJvdNTbleplIm9PxMXX+szHaglzXVX1JJeuF2JHdsW/+Z6yoZx6/Kvref6fJBYWStfLg8LxsaoY7jr/sEqIs6mRvndUEVlPKQIqj7LwokjRLepJxZKrUDryY3fT6qVl5fl6g3'
    payment_method = "VIET_QR"
    amount = 90000
    payer_name = '123'
    payer_account = '123123123'
    payer_bank = '123123'
    transaction_pay_in(env, merchant_id, merchant_secret, private_key, payment_method, amount, payer_name, payer_account,payer_bank)

