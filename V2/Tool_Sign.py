import base64
import json
import uuid

import pytz
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from datetime import datetime

from bean.AreaEnum import AreaEnum
from bean.AreaEnum import CurrencyEnum
from bean.MerchantReq import MerchantReq
from bean.MoneyReq import MoneyReq
from bean.TradePayInReq import TradePayInReq


def checkSha256RsaSignature(content, signature, publicKeyStr):
    try:
        public_key = serialization.load_pem_public_key(publicKeyStr.encode('utf-8'))

        data_to_verify = content.encode('utf-8')
        signature_bytes = base64.b64decode(signature)
        public_key.verify(
            signature_bytes,
            data_to_verify,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print("error:" + str(e))  # Convert the exception object to a string and print it
        return False

def generate_32bit_uuid():
    # Generate a UUID
    unique_id = uuid.uuid4()
    # Convert the UUID to a 32-character string (remove dashes)
    uuid_str = str(unique_id).replace('-', '')
    return uuid_str

# Generating Signatures with Crypto
def sha256RsaSignature(privateKey, message):
    private_key = RSA.importKey(base64.b64decode(privateKey.encode('utf-8')))
    cipher = PKCS1_v1_5.new(private_key)
    h = SHA256.new(message.encode('utf-8'))
    signature = cipher.sign(h)
    return base64.b64encode(signature).decode('utf-8')


def minify(pay_in_req):
    return json.dumps(pay_in_req, default=lambda o: o.__dict__, separators=(',', ':'))


def get_formatted_datetime(timezone_str):
    # Creating a time zone object
    timezone = pytz.timezone(timezone_str)
    # Get the current time and set it to the specified time zone
    now = datetime.now(timezone)
    # Returns a formatted date and time string
    return now.isoformat(timespec='seconds')


# test demo
private_key_str = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC3LbmfPhjGXJ+a6NVKyRWEfCpsKfl9UFnMRltNosJv+7qd6OUK3t7Q8fKX8rxuJBeXLLWrOZvjoGlP3ybvvhUSGKH+BLcN1k2eJbcKuThvXvKQvd7pXolY91gkF8V78FX+TKegZupbeji0XUGXCBNyShocYM6Cvailf0Iyv49dcktJmi4drBKfgj5l4HUY9TaDuCZOrhvFZfZZxBK1zkm72k0ZLfqTGmG8O2tsByndCTH2aPLT9odR8/O4qfoTG+vV9HivIKKOI2h0kZfQBOqWD4/ofwu9PNoRRzGgzfRpF3GhnKa3bRVSpCUuBtHfotQfFxbjaDk0s3K5BhQE7HxzAgMBAAECggEARHhaBxUeC595pVzcxVyOp3wGG3JBKL9NIZc277kj9tngcsAoRTzziqS1qmh4WK8zBjYXHg6ln5tJYiqmkjy6AY6llp7KkeiGENRGLEL5vl9+Se4/EXpd2pxyHOOp1N8MNccPbVyqw1DXO0wUhVDme/UI94yUBLjB/kKoSvHhs+qwJ8cz9C8sF3Zs/zF6Te/f+Z+HrIbVj4vlx6DYBs3pWe7J+XYg3XXpbvIBJVTN0lreQAjtopic0F7o1EULnllJmOqy+kiRMuSi5ESrWFOnuCrY0iz/C8LJKlqWa3d+1jVLPvKYucXvddYrwjyu8kYHZAenKWKkLPlQkQxGUFcX8QKBgQDYSCsgg7tDlXTw1P9Z2BhkVo1ugYWA1FcxqTY2sTOMOwCTt3QZAFEqofbNvdjZbk7vu8gh5LyxbWAr/sNqOXH5915a6DZKBGl+qBTH2TZZKmhCUWlmn8T7ySYclfsgIZsUxHaDfY+otiXGtNegSX9US9/AFVSMdiQBCmr5/i48mQKBgQDY0U5+MDl6GnbDH/hCT+YMq/m5W58m7ehJfG6jPtLQkPPvMq2Oj5HUeXx4vDdUxzaRlC9fICwe2KgKiGYpJsRPte6JfO6te7wsO2lDk0oBiw+jewm4CwZ5KeDYyReha8Hc2H1j5hllVx5DIZiage2ZswS5+kCNgzf4QbdAOd886wKBgAo5TyCYWY/WTtLbnr6GgpCrrr/ci40NfJmyYAex1Lf6Sgqxj2FnLG8RfPM42DlfB4g5njpL78eLXhJ2VpJ86LBiSymM9JQHJV2BYIoZ8IHCiW8pHgxl3Q/x8EVFqbtZG1Wd++Q3WUUmZx6/ibnf/47ij08rMvX417bc4TW0GEdxAoGAPX3nUBynQH0e76oyg8QbT766nZphoe3ZcnYK/tuDeMmTlWR/Gq6XQnaOGcPvwWiajmFDqiv6t2jlB8+1gbhP9vd3RqEbJDKypKzY5uRwGc3xyoDLudnOpTB+Z51oyUxBeDwiG+IXk8lIeOufVzrAQ1YlYgWap0fu6MbijSGcsa8CgYEA0OolBxRKdBSxmwMbXDocg5HtHd15UgJdlgL9GFjDZPisUvM7LWK97E5QPhY2IEIcv0EW9jM62bc1uPMhwDuN1dzmLafQIivGsIj5qUy18CoE4KJHsTeKLeHkrd6/nBd4da4A37+ksJ1t/sgZpjl40ShrxTV+OtzzY/kuQ4Uqc9g="

publicKeyStr = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAty25nz4YxlyfmujVSskVhHwqbCn5fVBZzEZbTaLCb/u6nejlCt7e0PHyl/K8biQXlyy1qzmb46BpT98m774VEhih/gS3DdZNniW3Crk4b17ykL3e6V6JWPdYJBfFe/BV/kynoGbqW3o4tF1BlwgTckoaHGDOgr2opX9CMr+PXXJLSZouHawSn4I+ZeB1GPU2g7gmTq4bxWX2WcQStc5Ju9pNGS36kxphvDtrbAcp3Qkx9mjy0/aHUfPzuKn6Exvr1fR4ryCijiNodJGX0ATqlg+P6H8LvTzaEUcxoM30aRdxoZymt20VUqQlLgbR36LUHxcW42g5NLNyuQYUBOx8cwIDAQAB
-----END PUBLIC KEY-----"""
merchant_secret = "6a58a603e5043290f4097ee4a7745661b3656932d4eebc3106b5dddc3af6e053"

# minify demo
money_req = MoneyReq(CurrencyEnum.IDR.name, 10000)
merchant_req = MerchantReq("20019", None, None)
pay_in_req = TradePayInReq("BCA", None, None, None, "order-1234566789", "minify demo",
                           None,
                           None,
                           None, None, None, money_req, merchant_req, None,
                           None, AreaEnum.INDONESIA.code)
minifyStr = minify(pay_in_req)
print("minifyStr: " + minifyStr)

timestamp = get_formatted_datetime('Asia/Bangkok')

sign_str_value = timestamp+ "|" + merchant_secret +"|" + minifyStr
print("sign_str_value: " + sign_str_value)

signature = sha256RsaSignature(private_key_str, sign_str_value)
print("signature", signature)

check_result = checkSha256RsaSignature(sign_str_value, signature, publicKeyStr)
print("check_result", check_result)
