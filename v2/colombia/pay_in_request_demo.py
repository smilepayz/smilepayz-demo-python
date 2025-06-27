import json

import requests

from v2.colombia import Tool_Sign
from v2.colombia.bean.AreaEnum import AreaEnum
from v2.colombia.bean.AreaEnum import CurrencyEnum
from v2.colombia.bean.Constants import Constants
from v2.colombia.bean.MerchantReq import MerchantReq
from v2.colombia.bean.MoneyReq import MoneyReq
from v2.colombia.bean.PayerReq import PayerReq
from v2.colombia.bean.TradePayInReq import TradePayInReq


def transaction_pay_in(env, merchant_id, merchant_secret, private_key, payment_method, amount,payer_name):
    global request_path
    print("=====> PayIn transaction")
    if env == "sandbox":
        # sandbox
        request_path = Constants.baseUrlSandbox + "/v2.0/transaction/pay-in"
    if env == "production":
        # production
        request_path = Constants.baseUrl + "/v2.0/transaction/pay-in"

    # transaction time
    timestamp = Tool_Sign.get_formatted_datetime('America/Lima')
    print("timestamp:" + timestamp)

    # partner_id
    merchant_order_no = merchant_id + Tool_Sign.generate_32bit_uuid()
    purpose = "Purpose For Transaction from python SDK"

    # moneyReq
    money_req = MoneyReq(CurrencyEnum.COP.name, amount)

    payer_req = PayerReq(payer_name, None, "")

    # merchantReq
    merchant_req = MerchantReq(merchant_id, "下雨天", None)

    pay_in_req = TradePayInReq(payment_method, payer_req, None, None, merchant_order_no[:32], purpose,
                               None,
                               None,
                               None, None, None, money_req, merchant_req, "https://ww.baidu.com",
                               "https://ww.baidu.com", AreaEnum.COLOMBIA.code)

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
    assert result['status'] in ['PROCESSING', 'SUCCESS', 'COMPLETED'], f"状态异常：{result['status']}"
    assert 'money' in result, "返回结果缺少money字段"
    assert 'amount' in result['money'], "money字段缺少amount"
    assert abs(result['money']['amount'] - amount) < 0.01, f"金额不匹配，返回金额：{result['money']['amount']}，请求金额：{amount}"
    assert 'currency' in result['money'], "money字段缺少currency"
    assert result['money']['currency'] == 'COP', f"币种错误，返回币种：{result['money']['currency']}"
    assert 'channel' in result, "返回结果缺少channel字段"
    assert 'paymentMethod' in result['channel'], "channel字段缺少paymentMethod"
    assert result['channel']['paymentMethod'] == 'CASHIER_CO', f"支付方式不匹配，返回支付方式：{result['channel']['paymentMethod']}"


# run
if __name__ == '__main__':
    env = 'production'
    merchant_id = '20158'
    merchant_secret = 'ebef0a7119b5208e84633f63dafd61110ae97e24ee4d120bb04045aa28111671'
    private_key = 'MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCEGyBGscdvb86+tKjGqVUdXv1NqVXz9H4PLdAZsdvW+rHKbr9SEFddDOi2qUiICIHyip3Y4qHKYVB4KcI5ZqknHpWh3dB32Khj4TMqM6YXe7BGaUeYoncjCBfFDDysX+a629cIFX4Fnu6VqbKkRJzRiwqQg7uhFwXhvtrHQfEGTo4Co2wC6B4MGLDEYZwDbBYRpGhLPQ9kDejuvdBLw50QY52ah3SpDC/oy9n8lT+BgL6bNod0xA6W2BuR63wwo1knz3uNDRwSReKvHtoGF58j/8oSk1cmctttWV6QIYyriynLDMRUVAst+JvgugJG6ae44MteullloPkXNdhUWCF7AgMBAAECggEAFzitc7/MTspYjS00fbdGPuNzozMg6MERZ5ml+t5IxoFKv0q4VrSIptKeFX2sQj08mmXDWVx9FBYHDxhIC87/7OBzbQCQpIBxGR184O4zQ+16DuZyr2Hfj0jc5MZB5Ar3g+Eg60rb3CETzzsFK9rjtfG66aw+TxK89fGWg3AT7gegRx35w01e1geLm0yPs1LS/aqj952jfUVdzTMMDRi7qccKoZ9QzCLcaKgFJFthIts2nq+bM2UixSVP/veQZoaLOBKXtPT6grviClebIrw0ocXOWfXwwDSL/ROu1j/0A8d9+PWoKhyIE2bZQhFoAsYEIrC86yeh6e5uqL6vMxjAAQKBgQC5pfrntQYKTA6VACm2touC89cnujOwoI46xLxPsbRF8Z2mETlLbGENiX+Xkd8p/glZJbe2FHdmKAaoQAsSyChJoH/840xRcUY4TIUkQhaNBpWxfiRynFspUb4LMpqg6sygjswj3Gt67fjC2fYJuvzNDEvE0/wKltvrmyZu4oXG2wKBgQC2KutXedBAeX9nysrZ7NI2TjW/zigOhW9vLHnUgnyoIY7CAq8sib4k9fR8c/Gx/0flmDOTcVvPUMWaVfmrlXtgoD9/6uS25uarq0ZjZwqBzeTCimHazYfHwrmjgAr1oCINffMXOqYGpsdjfrTQRqK+v1F6i1p2PVb+v1G5Z7CB4QKBgCM2r4vp01Z6rL1ohYEJyRayx9naQNm86p2NGacILwihVuTcGYEL8rDNpu0KF0lwzTcip2EbKrau2uxpEXCjlLi6f+xo9N3x3X7qTMre2kYvvI8pPSKcM9J3ldOr6pahUuUVkPUwZxavMuNK0pdv52nBblHMX99mVBqxmC2qO/PHAoGAJaTy4y3KCjjRSjqO9r/IpO4+jzdj8bRDVd8EAhVA+2GL5a22U2bXgz3MWxd+n8DYM6rjJZnsVggj/YO8x2dpiosy9BUvVFic3GbVcd8uPaq1ljoQhK2qXG5x/EaOfTmtL8qSPH+jJYa7d2UMqmmeYfqZNNCtTffZDWWt1rmFsSECgYEApRmch1TBZKNO/zfTQkE133sQXFx4MyUZEP/0i9kYUIHdCzYCfKhFBcUuuED588VMqZKApZbI7BaxSddBrr73vq4rt9kNzVnPuCHpY9Y086WLOnIPqngUgDq39gAq7awyPBvin5pdRVoXJm2iOOjJOBCP/zDfQybaIuyx6ZMISIs='
    payment_method = "CASHIER_CO"
    amount = 10000
    payer_name = "sonia"
    transaction_pay_in(env, merchant_id, merchant_secret, private_key, payment_method, amount,payer_name)
