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


def transaction_pay_in(env, merchant_id, merchant_secret, private_key, payment_method, amount, pix_account):
    global request_path
    print("=====> PayIn transaction")
    if env == "sandbox":
        # sandbox
        request_path = Constants.baseUrlSandbox + "/v2.0/transaction/pay-in"
    if env == "production":
        # production
        request_path = Constants.baseUrl + "/v2.0/transaction/pay-in"

    # transaction time
    timestamp = Tool_Sign.get_formatted_datetime('America/Sao_Paulo')
    print("timestamp:" + timestamp)

    # partner_id
    merchant_order_no = merchant_id + Tool_Sign.generate_32bit_uuid()
    purpose = "Purpose For Transaction from python SDK"

    # moneyReq
    money_req = MoneyReq(CurrencyEnum.BRL.name, amount)

    # merchantReq
    merchant_req = MerchantReq(merchant_id, "your merchant name", None)#增加一个子商户submerchanid

    # merchant_req = MerchantReq(merchant_id, "your merchant name", None,2015801)#增加一个子商户submerchanid


    # payerReq
    payer_req = PayerReq(None, None, None, pix_account)

    pay_in_req = TradePayInReq(payment_method, payer_req, None, None, merchant_order_no[:32], purpose,
                               None,
                               None,
                               None, None, None, money_req, merchant_req, "https://www.baidu.com",
                               "https://www.baidu.com")

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
    assert result['code']=='00',f"接口调用失败，code={result['code']},message={result.get( 'message')}"
    assert 'tradeNo' in result and result['tradeNo'], 'tradeNo缺失或为空'
    assert 'orderNo' in result and result['orderNo'], "orderNo缺失或为空"
    assert 'status' in result, "返回结果缺少status字段"
    assert result['status'] in ['PROCESSING', 'REVIEW'], f"状态异常：{result['status']}"
    assert 'money' in result, "返回结果缺少money字段"
    assert 'amount' in result['money'], "money字段缺少amount"
    assert abs(result['money']['amount'] - amount) < 0.01, f"金额不匹配，返回金额：{result['money']['amount']}，请求金额：{amount}"
    assert 'currency' in result['money'], "money字段缺少currency"
    assert result['money']['currency'] == 'BRL', f"币种错误，返回币种：{result['money']['currency']}"
    assert 'channel' in result, "返回结果缺少channel字段"
    assert 'paymentMethod' in result['channel'], "channel字段缺少paymentMethod"
    assert result['channel']['paymentMethod'] == 'PIX', f"支付方式不匹配，返回支付方式：{result['channel']['paymentMethod']}"



# def get_public_ip():
# # 通过公共API获取公网 IP
#     response = requests.get("https://api.ipify.org")
#     return response.text
#
# public_ip = get_public_ip()
# print("公网 IP 地址为:", public_ip)


if __name__ == '__main__':
    env = 'production'
    # merchant_id = '20158'
    # merchant_secret = 'ebef0a7119b5208e84633f63dafd61110ae97e24ee4d120bb04045aa28111671'
    # private_key = 'MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDDUFDuFqO8Q9Dr0xmHTSNoWDG1nwX3rroX5oUdpUrP1jUTejyb4pQ6Yim9o4Fh1pbrHa1499d7tGgPycSq5uFzv9O+jkSSRbnUvM4nh+ktpvBwWPw6vTYP/8pZ88yzXzDdIO6bXN0XkcM44cCfmohkldIdg2DO+i8H15opilVqDCGFgi/peK/bOsN/Nw6VMHAacITBHfJhFqSSgJQgHCc+H1OTjN7TWmGkPBi8Alpzcl6ZWBFIMT35m5hy7OPY4In1/MnytyQG+wOYiVmSzxg5E2S9vooKANpybmLuBI0T32ZEpNevSUwySlFfFXB52QIDbaZKAy4Jc7wuNbc9o6WLAgMBAAECggEALpaLX2deEgu5G29kwP3Y6sxSuyheA4kVkZrmeL5TPIUzbtxy9ZoT0mNU4ovMUlqd8CJJnTe9GiBbzBxMQZnGAFaq+uKzn5JrM7//irVkHQQbiSjorVgxu5o/mbpKQyT7Ilv3Hm8Fu9gEkZ5j1I5HZ3rHPkv2vRg3PK8kcjExk5Q66tmwx4Trhy4UbwPVWcFkf10bHpkQPBBBtAwXqPMFnG0e91pE8EVrfvGECEDSSp/hqTKLzoeWsJcRJH0DdA8Z1WGtEXCrNOlFvm0b1s3ZBuoUS9fGCoysq3Fqz1b4dAmO19kIaUUIqkHAjNBmEftC3FbivL+RPXmWww94QbhkwQKBgQD4jyRvfr5IAbqa6Da5ltbJkIF73EAM+7gVYpeDJI2rW3Twj9yLzOcuHthdXum7cvJ/Kqn5a3SwEvNHTXgLozlKD+wUUM/dQIgVMZIgGGTWEDox8ifjJxsxo9bOt8hkNV3ENtpXpbcXSlgDW1/vWJNGU/dISI/MS8zH209bLFDdwQKBgQDJKR9OqjDL0wWnrOI11iSOEZNaa1Yh51rpSKAXQyAh3/OXAlNgc/WmMnw02HwOaOLpNz5RW44Zi6z2yCi0ZM653lPPwjfFXp/jsF/KPqOcRe5DS6YUgtbeP6SzRe9kRgL3LbfkghvM0IWUGnCevXAiMLDN4IeZLGHZ9K8iVJouSwKBgARy428PcK5vQXzGTTxzI7MF4BtsbMUOuFPBqP6S5+o6P9SSbpsd9sFPkgXRzhMp0odOJy6sqrEAFdSf4Vcr+7mEoXAXpjDKl+TxNzFV3nAqaDA+qlIZgBYaXZzjkzWf8uaxKKVK9QT4sqyUtRnelvw6QoHLsq8waCDnnvr9xxDBAoGBAJS6kcowrQlWSV0SxuG1JavgtMjqiXFhw+ataqgoWi6RjWF+N7Udp2cs9oZ/9SEWTYbO8IVoouSiT8zaarYNvobQKbl3SJLmBmNq+TfoHkGhtqsM2ItbvY/vEE/4CipiVTj6FXee9vz0w36gGdpUB/9PbrmZI8iNdv+WGJLSaHiHAoGBAKkTd+OzbkanMW8E/NLx7z+i98J4b83J5T6nf4UlJvdNTbleplIm9PxMXX+szHaglzXVX1JJeuF2JHdsW/+Z6yoZx6/Kvref6fJBYWStfLg8LxsaoY7jr/sEqIs6mRvndUEVlPKQIqj7LwokjRLepJxZKrUDryY3fT6qVl5fl6g3'

    merchant_id = '20190'
    merchant_secret = '8decca074fa734af3b74bf3ee2de50bdce56f715cbc7e3788b59b72d8fb4776d'
    private_key = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCbr/c44T8qWI2k6i+yZFJfFhhhnEu9Fu69g5o9UgKui8W/+18pCt9LEgSjQGgxFJe6C8X18kAXoxfstIkkSnL7q55/rXyNkymOmwpRXoO8ApgCNIlSHISKgUhaDm5pZvFvNn2u9Rsyhv9HYlf4D+e+1MkoD1dRQeefoO9nQTE5fA4uqpiKBvu7q9FJyUMI8+57ZWOddReWhLWpEkNlyDglAzdSy+wObIBx0hgKRdPWgOpuSDsSnjoAdb1+dA2PKjicAcwJOJKVAohiT70xJHnnAYFVn4w8SzkordhqV6R4XDzhnJMWr8FCPHYFvypfDKz2ZLn4pzXxVRWkPHYwlTCXAgMBAAECggEARzljYpQ5r4e/lTjGBVi8DmAvW0iDpcf+BJlWUMNaErxDBadcS4x7xv5BPOZURE/lcem88N2Y0Ld+VH3rV7zviY9j/YlCuAohMupe+AbDQZn2LNwYDoaZZDvs+7YqcPH1dil5qjbb8GuuEdw93nB4VudF95u9GKGL841OuPAsMt2FfMKnqlmbIadIp3lwgk1eTrrfykCksGS4S2lL9uixX6V2tF9zXW/fLmFIJ7xHtjgofhZsJQown2pQrNnxBibWk2lDd5fpTKooPsHp6CPBlUzTtacaCvjqV/vOgtUiql74hL2Mbq9rXCMykkmaIpLt0NbStwir/1oo3G2wuTDiMQKBgQDITFywS/sZ4vA5hz4NkzlFS0M7VoVZ3oysfPnNzyU6J2uE1+VKyTM1ncJegOScriYo238Gnbu30Jq1kY2iNFBDqveSgErkhNF8b1pdBqknRIOgHcf9Kz96L5K6Pu3gZFnWXC+qbM47cLIfk55es/LvN7kQGNH5fVaqjFfsbu2yJQKBgQDG+6mOK47vU51dMlzT/LBkeD04RL83sK6dxkCYbG8cLf+bcdlLjcXl+E/PUW6bxUIgCm+ib73mBZ3K2TAkNjA9f83mzpcpIbM3WctX/FNh27rjDu+Wswd/6tzMyuoey4EASMAmFlZyrdhJqNuuhD3SRfLK77yemAq2PmndZEOVCwKBgH5Jr1M0xOCAdqg+/j/+6GgpWP2Lws50BEwpDDPYfIdbHW6H1Tk+/Hu8uTVunTWwk7zFECUyxI3UCAec+ykfRNA1dp03KIFGwPJtHxNyRKrOhxMoU9TrNL2sSx4E2WTWwNHoE+GncqyFlLlWEM9zNCPiBVwB2jos7bzgeftHwbTFAoGBAMbwANrk7aiU3jW5DlnavrgUBpDlGpAhEtMmzJoXfxabXnwY3PjOq1Z6ZcCOV5lhI/VIucebFC6O2u1dKuZpTt2Nk1v4m+RBjx39pnE3El46AqTT3/G41/yp4UrWbC+Rok2YbpMlrhRFfoJWUhwulmhOCqmd+eRNehguWkU/4tl1AoGAOPrbWPkU7qGrA6KWJ5BspjTECflVh304nRhxTO+kprdHN0/HbEZkJrsV+igzftsM7RWwdJUqK9kkJ7YdLsFGbZFlCdcdcJ4rUjY+1IFobSKu1QG0EHlsiu26l1rc8hKxxdTC6o71d6D7KVyzE1/pFBxFa6HnB9c7wCoSi4Gq/ZA="

    # env = 'sandbox'
    # merchant_id = 'sandbox-20158'
    # merchant_secret = '5439857241094fbb0c125ea9dc287e2935c9b43a931dbf2030c30c6c76f23703'
    # private_key = "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDLZzB9/V23ugUgqxOIqA4J7s311OlEjxCVDFBiKnwCFpXp2DkjrVGrSTkBcwq/QrqM+g/I0Jea+iW3OTNutUjoIIyzicGuFneysFVNcv9S7zRONmeHe6pcLiwnZws6EQILIIFhZyAZ2zG7JQw8tEPMFVj9dXha+6Y7TZIyvTx7mH6M+fC4P6KXzX+mn4WVW7EmVF06MPed6XbrM8mw7UMFKnt7iMPTfc9FXBJZGOtg+bkIV4KcxQR6LPUmuuQA7X/hxCKjRRQ8FZE2ZDjLN5MI5QxigBYfmKubRzKWvC4rbxrBkEzBRpzn4+6eMyh5MESN7jnxu+az1lt3TBO4EjSHAgMBAAECggEAWS9AIGX48yeBuw637Gn/adSHAxydQT3Xf/rbvgcxw3qitdtkRmPm1MswzxVhp3X7NPgp9pubdczrv5g5mHetZXZsKwaiYRIh3rwZUvGyyOrwTMDnCQ0sp+lo28f/MLEna7iPciVU+nFVL2DxqiZCOdg8YjnhEUeY3hTHny7BN9Ffw1//i4uoUvYl7J5Cev01kqrNcaUPjyjiC491aytx3Zwj02bHwQYqHgxgyxUJjwqudzl9r3jMJkDQTgkj8TovuzIdTmBO01FnnAOzj0CIm4jlYO5BavoBISUqx7JdeXtSjNqsIOEEOcfzY1J48wP6ZggH07kB46ZN6Z/4efI3xQKBgQDk+gGwakBz9Qafd2mA8nj5mXB7kk1pzui5yJWKQSwkqtzBCxwLeCecOwoQzjUtNG4+iWSjXMXkMIEYqUPn9LDmMO0/gXk+iiXscZnIw9T+Cg8XBi1X73lvlkr+iR4Bo1Dys4hHtwYKw7xf1OWakazvXub8S751yGNPJ4Gs5giC8wKBgQDjaIn+/36nzc6K9KNgsY1lfx9mg4pv3lTAdpM1vhmVQjEZrJ7rijGIpd5lvHW9XNL8OQqbJGkXXFTLb3p31lra6vv88y4BARfzy5lLuKXeBmrLdZ5hXVyesCFZcwM2SKcslViBu3BaPXQ9NcmCby+4Ntwa/+mxkwFSXM63kijlHQKBgQCHk0/0uLS489ecDAQ4CVl/0E49nH6hq5U4i3+fgL82ZsSWuJE+aUJqyrpHARGTVnwAIzGnWIMDfYSyqWY/rS4g3c9bzrmPQhT6TrkTmoA+eo48v7eRXYW1gHOfCmjt51lCmvKSI9g7/3FF/LSGNMMEaFi0AdUfwCqs72NkkD9x6QKBgQCdx+ePHHglN19p/AjrSuW/GS+RMg04Rvtouhyzeh1H+TAWDzYIWM67b9JZpiPO6fudcnpQYDfmNHLE36kKQpixMb76p0MxATA8P/QxnIDBBpTMa+Qiy+M6WxwYcvs0i74p6ckJ4iI3ClJ/MbWJoVlrp+yZcxwSz9tn6OqoZWmoZQKBgC+5LH2He3CagoKHkF155/0CXbTnrLvHxrlPid47spbYBg5/vboimDXlMbmNmrviEGsA1YMCDuUyr/nzNg/kIPME6FiBA9cSD5n/r7nudqulw9mRmcBK52i6dDkXJoEfaOxsJ9JzTBLxPX8+titvGKkyDaNyPsQ1igVsgm81Jx6Q"
    payment_method = 'PIX'
    amount = 1500
    pix_account = '12345678909'
    transaction_pay_in(env,merchant_id,merchant_secret,private_key,payment_method,amount,pix_account)


















