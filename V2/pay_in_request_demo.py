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

private_key_str = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC3LbmfPhjGXJ+a6NVKyRWEfCpsKfl9UFnMRltNosJv+7qd6OUK3t7Q8fKX8rxuJBeXLLWrOZvjoGlP3ybvvhUSGKH+BLcN1k2eJbcKuThvXvKQvd7pXolY91gkF8V78FX+TKegZupbeji0XUGXCBNyShocYM6Cvailf0Iyv49dcktJmi4drBKfgj5l4HUY9TaDuCZOrhvFZfZZxBK1zkm72k0ZLfqTGmG8O2tsByndCTH2aPLT9odR8/O4qfoTG+vV9HivIKKOI2h0kZfQBOqWD4/ofwu9PNoRRzGgzfRpF3GhnKa3bRVSpCUuBtHfotQfFxbjaDk0s3K5BhQE7HxzAgMBAAECggEARHhaBxUeC595pVzcxVyOp3wGG3JBKL9NIZc277kj9tngcsAoRTzziqS1qmh4WK8zBjYXHg6ln5tJYiqmkjy6AY6llp7KkeiGENRGLEL5vl9+Se4/EXpd2pxyHOOp1N8MNccPbVyqw1DXO0wUhVDme/UI94yUBLjB/kKoSvHhs+qwJ8cz9C8sF3Zs/zF6Te/f+Z+HrIbVj4vlx6DYBs3pWe7J+XYg3XXpbvIBJVTN0lreQAjtopic0F7o1EULnllJmOqy+kiRMuSi5ESrWFOnuCrY0iz/C8LJKlqWa3d+1jVLPvKYucXvddYrwjyu8kYHZAenKWKkLPlQkQxGUFcX8QKBgQDYSCsgg7tDlXTw1P9Z2BhkVo1ugYWA1FcxqTY2sTOMOwCTt3QZAFEqofbNvdjZbk7vu8gh5LyxbWAr/sNqOXH5915a6DZKBGl+qBTH2TZZKmhCUWlmn8T7ySYclfsgIZsUxHaDfY+otiXGtNegSX9US9/AFVSMdiQBCmr5/i48mQKBgQDY0U5+MDl6GnbDH/hCT+YMq/m5W58m7ehJfG6jPtLQkPPvMq2Oj5HUeXx4vDdUxzaRlC9fICwe2KgKiGYpJsRPte6JfO6te7wsO2lDk0oBiw+jewm4CwZ5KeDYyReha8Hc2H1j5hllVx5DIZiage2ZswS5+kCNgzf4QbdAOd886wKBgAo5TyCYWY/WTtLbnr6GgpCrrr/ci40NfJmyYAex1Lf6Sgqxj2FnLG8RfPM42DlfB4g5njpL78eLXhJ2VpJ86LBiSymM9JQHJV2BYIoZ8IHCiW8pHgxl3Q/x8EVFqbtZG1Wd++Q3WUUmZx6/ibnf/47ij08rMvX417bc4TW0GEdxAoGAPX3nUBynQH0e76oyg8QbT766nZphoe3ZcnYK/tuDeMmTlWR/Gq6XQnaOGcPvwWiajmFDqiv6t2jlB8+1gbhP9vd3RqEbJDKypKzY5uRwGc3xyoDLudnOpTB+Z51oyUxBeDwiG+IXk8lIeOufVzrAQ1YlYgWap0fu6MbijSGcsa8CgYEA0OolBxRKdBSxmwMbXDocg5HtHd15UgJdlgL9GFjDZPisUvM7LWK97E5QPhY2IEIcv0EW9jM62bc1uPMhwDuN1dzmLafQIivGsIj5qUy18CoE4KJHsTeKLeHkrd6/nBd4da4A37+ksJ1t/sgZpjl40ShrxTV+OtzzY/kuQ4Uqc9g="
public_key_str = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAty25nz4YxlyfmujVSskVhHwqbCn5fVBZzEZbTaLCb/u6nejlCt7e0PHyl/K8biQXlyy1qzmb46BpT98m774VEhih/gS3DdZNniW3Crk4b17ykL3e6V6JWPdYJBfFe/BV/kynoGbqW3o4tF1BlwgTckoaHGDOgr2opX9CMr+PXXJLSZouHawSn4I+ZeB1GPU2g7gmTq4bxWX2WcQStc5Ju9pNGS36kxphvDtrbAcp3Qkx9mjy0/aHUfPzuKn6Exvr1fR4ryCijiNodJGX0ATqlg+P6H8LvTzaEUcxoM30aRdxoZymt20VUqQlLgbR36LUHxcW42g5NLNyuQYUBOx8cwIDAQAB"
merchant_code_sandbox = "6a58a603e5043290f4097ee4a7745661b3656932d4eebc3106b5dddc3af6e053"
merchant_code = "95b57c46b8c2e068982be23fb669a80612cad68e6ce6ba4f5af9ec20d23bb274"
merchant_id_sandbox = "sandbox-20019"
merchant_id = "20019"


def transaction_pay_in():
    print("=====> step3 : PayIn transaction")

    # url
    path_url = "https://gateway-test.smilepayz.com/v2.0/transaction/pay-in"
    path_url_sandbox = "https://sandbox-gateway-test.smilepayz.com/v2.0/transaction/pay-in"

    # transaction time
    timestamp = Tool_Sign.get_formatted_datetime('Asia/Bangkok')
    print("timestamp:" + timestamp)

    # partner_id
    merchant_order_no = "T_" + str(time.time())
    purpose = "Purpose For Transaction from python SDK"
    # https://docs-test.smilepayz.com/en/reference/version1.0/data/paymentMethod_Brazil.html
    # https://docs-test.smilepayz.com/en/reference/version1.0/data/paymentMethod_India.html
    # https://docs-test.smilepayz.com/en/reference/version1.0/data/paymentMethod_Indonesia.html
    # https://docs-test.smilepayz.com/en/reference/version1.0/data/paymentMethod_Thailand.html
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
    pay_in_req = TradePayInReq(payment_method, None, None, None, merchant_order_no, purpose,
                               None,
                               None,
                               None, None, None, money_req, merchant_req, None,
                               None, AreaEnum.INDONESIA.code)

    # jsonStr by json then minify
    json_data_minify = json.dumps(pay_in_req, default=lambda o: o.__dict__, separators=(',', ':'))
    print("json_data_minify=", json_data_minify)

    # build
    string_to_sign = timestamp + "|" + merchant_code + "|" + json_data_minify
    print("string_to_sign=", string_to_sign)

    # signature
    signature = Tool_Sign.sha256RsaSignature(private_key_str, string_to_sign)
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
    response = requests.post(path_url, data=json_data_minify, headers=headers)
    # Get response result
    result = response.json()
    print(result)



# run
transaction_pay_in()
