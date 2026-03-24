import json

import requests

from v2.indonesia import Tool_Sign
from v2.indonesia.bean.AreaEnum import AreaEnum
from v2.indonesia.bean.AreaEnum import CurrencyEnum
from v2.indonesia.bean.Constants import Constants
from v2.indonesia.bean.MerchantReq import MerchantReq
from v2.indonesia.bean.MoneyReq import MoneyReq
from v2.indonesia.bean.TradePayoutReq import TradePayoutReq


def pay_out_request_demo(env, merchant_id, merchant_secret, private_key, payment_method, amount, cash_account):
    global request_path
    if env == "production":
        # production
        request_path = Constants.baseUrl + "/v2.0/disbursement/pay-out"
    if env == "sandbox":
        # sandbox
        request_path = Constants.baseUrlSandbox + "/v2.0/disbursement/pay-out"

    # transaction time
    timestamp = Tool_Sign.get_formatted_datetime('Asia/Jakarta')
    print("timestamp:" + timestamp)
    # partner_id
    merchant_order_no = merchant_id + Tool_Sign.generate_32bit_uuid()
    purpose = "Purpose For Transaction from python SDK"

    # moneyReq
    money_req = MoneyReq(CurrencyEnum.IDR.name, amount)
    # merchantReq
    merchant_req = MerchantReq(merchant_id, "your merchant name", None,'2019002')

    # payInReq
    pay_in_req = TradePayoutReq(payment_method, None, None, cash_account, merchant_order_no[:32], purpose,
                                None,
                                None,
                                None, None, None, money_req, merchant_req, "",
                                None)

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

    # 断言
    assert result is not None, "接口未返回数据"
    assert result.get('code') == '00', f"接口调用失败，code={result.get('code')}"
    assert result.get('status') in ['REVIEW', 'PROCESSING'], f"状态异常，status={result.get('status')}"
    assert 'tradeNo' in result and result['tradeNo'], "缺少tradeNo"
    assert 'orderNo' in result and result['orderNo'], "缺少orderNo"
    assert result.get('money', {}).get('currency') == 'IDR', f"币种错误，currency={result.get('money', {}).get('currency')}"
    assert isinstance(result.get('money', {}).get('amount'), (int, float)), "金额不合法"
    assert result.get('channel', {}).get('paymentMethod') == 'ANZ', f"支付方式错误，paymentMethod={result.get('channel', {}).get('paymentMethod')}"


# run
if __name__ == '__main__':
    # env = 'production'
    # merchant_id = '20158'
    # merchant_secret = 'ebef0a7119b5208e84633f63dafd61110ae97e24ee4d120bb04045aa28111671'
    # private_key = 'MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDDUFDuFqO8Q9Dr0xmHTSNoWDG1nwX3rroX5oUdpUrP1jUTejyb4pQ6Yim9o4Fh1pbrHa1499d7tGgPycSq5uFzv9O+jkSSRbnUvM4nh+ktpvBwWPw6vTYP/8pZ88yzXzDdIO6bXN0XkcM44cCfmohkldIdg2DO+i8H15opilVqDCGFgi/peK/bOsN/Nw6VMHAacITBHfJhFqSSgJQgHCc+H1OTjN7TWmGkPBi8Alpzcl6ZWBFIMT35m5hy7OPY4In1/MnytyQG+wOYiVmSzxg5E2S9vooKANpybmLuBI0T32ZEpNevSUwySlFfFXB52QIDbaZKAy4Jc7wuNbc9o6WLAgMBAAECggEALpaLX2deEgu5G29kwP3Y6sxSuyheA4kVkZrmeL5TPIUzbtxy9ZoT0mNU4ovMUlqd8CJJnTe9GiBbzBxMQZnGAFaq+uKzn5JrM7//irVkHQQbiSjorVgxu5o/mbpKQyT7Ilv3Hm8Fu9gEkZ5j1I5HZ3rHPkv2vRg3PK8kcjExk5Q66tmwx4Trhy4UbwPVWcFkf10bHpkQPBBBtAwXqPMFnG0e91pE8EVrfvGECEDSSp/hqTKLzoeWsJcRJH0DdA8Z1WGtEXCrNOlFvm0b1s3ZBuoUS9fGCoysq3Fqz1b4dAmO19kIaUUIqkHAjNBmEftC3FbivL+RPXmWww94QbhkwQKBgQD4jyRvfr5IAbqa6Da5ltbJkIF73EAM+7gVYpeDJI2rW3Twj9yLzOcuHthdXum7cvJ/Kqn5a3SwEvNHTXgLozlKD+wUUM/dQIgVMZIgGGTWEDox8ifjJxsxo9bOt8hkNV3ENtpXpbcXSlgDW1/vWJNGU/dISI/MS8zH209bLFDdwQKBgQDJKR9OqjDL0wWnrOI11iSOEZNaa1Yh51rpSKAXQyAh3/OXAlNgc/WmMnw02HwOaOLpNz5RW44Zi6z2yCi0ZM653lPPwjfFXp/jsF/KPqOcRe5DS6YUgtbeP6SzRe9kRgL3LbfkghvM0IWUGnCevXAiMLDN4IeZLGHZ9K8iVJouSwKBgARy428PcK5vQXzGTTxzI7MF4BtsbMUOuFPBqP6S5+o6P9SSbpsd9sFPkgXRzhMp0odOJy6sqrEAFdSf4Vcr+7mEoXAXpjDKl+TxNzFV3nAqaDA+qlIZgBYaXZzjkzWf8uaxKKVK9QT4sqyUtRnelvw6QoHLsq8waCDnnvr9xxDBAoGBAJS6kcowrQlWSV0SxuG1JavgtMjqiXFhw+ataqgoWi6RjWF+N7Udp2cs9oZ/9SEWTYbO8IVoouSiT8zaarYNvobQKbl3SJLmBmNq+TfoHkGhtqsM2ItbvY/vEE/4CipiVTj6FXee9vz0w36gGdpUB/9PbrmZI8iNdv+WGJLSaHiHAoGBAKkTd+OzbkanMW8E/NLx7z+i98J4b83J5T6nf4UlJvdNTbleplIm9PxMXX+szHaglzXVX1JJeuF2JHdsW/+Z6yoZx6/Kvref6fJBYWStfLg8LxsaoY7jr/sEqIs6mRvndUEVlPKQIqj7LwokjRLepJxZKrUDryY3fT6qVl5fl6g3'
    # payment_method = "BRI"
    # amount = 50000
    # cash_account = "1231234353"
    # pay_out_request_demo(env, merchant_id, merchant_secret, private_key, payment_method, amount, cash_account)

    env = 'production'
    merchant_id = '20190'
    merchant_secret = '8decca074fa734af3b74bf3ee2de50bdce56f715cbc7e3788b59b72d8fb4776d'
    private_key = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCbr/c44T8qWI2k6i+yZFJfFhhhnEu9Fu69g5o9UgKui8W/+18pCt9LEgSjQGgxFJe6C8X18kAXoxfstIkkSnL7q55/rXyNkymOmwpRXoO8ApgCNIlSHISKgUhaDm5pZvFvNn2u9Rsyhv9HYlf4D+e+1MkoD1dRQeefoO9nQTE5fA4uqpiKBvu7q9FJyUMI8+57ZWOddReWhLWpEkNlyDglAzdSy+wObIBx0hgKRdPWgOpuSDsSnjoAdb1+dA2PKjicAcwJOJKVAohiT70xJHnnAYFVn4w8SzkordhqV6R4XDzhnJMWr8FCPHYFvypfDKz2ZLn4pzXxVRWkPHYwlTCXAgMBAAECggEARzljYpQ5r4e/lTjGBVi8DmAvW0iDpcf+BJlWUMNaErxDBadcS4x7xv5BPOZURE/lcem88N2Y0Ld+VH3rV7zviY9j/YlCuAohMupe+AbDQZn2LNwYDoaZZDvs+7YqcPH1dil5qjbb8GuuEdw93nB4VudF95u9GKGL841OuPAsMt2FfMKnqlmbIadIp3lwgk1eTrrfykCksGS4S2lL9uixX6V2tF9zXW/fLmFIJ7xHtjgofhZsJQown2pQrNnxBibWk2lDd5fpTKooPsHp6CPBlUzTtacaCvjqV/vOgtUiql74hL2Mbq9rXCMykkmaIpLt0NbStwir/1oo3G2wuTDiMQKBgQDITFywS/sZ4vA5hz4NkzlFS0M7VoVZ3oysfPnNzyU6J2uE1+VKyTM1ncJegOScriYo238Gnbu30Jq1kY2iNFBDqveSgErkhNF8b1pdBqknRIOgHcf9Kz96L5K6Pu3gZFnWXC+qbM47cLIfk55es/LvN7kQGNH5fVaqjFfsbu2yJQKBgQDG+6mOK47vU51dMlzT/LBkeD04RL83sK6dxkCYbG8cLf+bcdlLjcXl+E/PUW6bxUIgCm+ib73mBZ3K2TAkNjA9f83mzpcpIbM3WctX/FNh27rjDu+Wswd/6tzMyuoey4EASMAmFlZyrdhJqNuuhD3SRfLK77yemAq2PmndZEOVCwKBgH5Jr1M0xOCAdqg+/j/+6GgpWP2Lws50BEwpDDPYfIdbHW6H1Tk+/Hu8uTVunTWwk7zFECUyxI3UCAec+ykfRNA1dp03KIFGwPJtHxNyRKrOhxMoU9TrNL2sSx4E2WTWwNHoE+GncqyFlLlWEM9zNCPiBVwB2jos7bzgeftHwbTFAoGBAMbwANrk7aiU3jW5DlnavrgUBpDlGpAhEtMmzJoXfxabXnwY3PjOq1Z6ZcCOV5lhI/VIucebFC6O2u1dKuZpTt2Nk1v4m+RBjx39pnE3El46AqTT3/G41/yp4UrWbC+Rok2YbpMlrhRFfoJWUhwulmhOCqmd+eRNehguWkU/4tl1AoGAOPrbWPkU7qGrA6KWJ5BspjTECflVh304nRhxTO+kprdHN0/HbEZkJrsV+igzftsM7RWwdJUqK9kkJ7YdLsFGbZFlCdcdcJ4rUjY+1IFobSKu1QG0EHlsiu26l1rc8hKxxdTC6o71d6D7KVyzE1/pFBxFa6HnB9c7wCoSi4Gq/ZA="
    payment_method = "QRIS"#BRI
    amount = 10000
    cash_account = "1231234353"
    # env = 'production'
    # merchant_id = '20190'
    # merchant_secret = '8decca074fa734af3b74bf3ee2de50bdce56f715cbc7e3788b59b72d8fb4776d'
    # private_key = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCbr/c44T8qWI2k6i+yZFJfFhhhnEu9Fu69g5o9UgKui8W/+18pCt9LEgSjQGgxFJe6C8X18kAXoxfstIkkSnL7q55/rXyNkymOmwpRXoO8ApgCNIlSHISKgUhaDm5pZvFvNn2u9Rsyhv9HYlf4D+e+1MkoD1dRQeefoO9nQTE5fA4uqpiKBvu7q9FJyUMI8+57ZWOddReWhLWpEkNlyDglAzdSy+wObIBx0hgKRdPWgOpuSDsSnjoAdb1+dA2PKjicAcwJOJKVAohiT70xJHnnAYFVn4w8SzkordhqV6R4XDzhnJMWr8FCPHYFvypfDKz2ZLn4pzXxVRWkPHYwlTCXAgMBAAECggEARzljYpQ5r4e/lTjGBVi8DmAvW0iDpcf+BJlWUMNaErxDBadcS4x7xv5BPOZURE/lcem88N2Y0Ld+VH3rV7zviY9j/YlCuAohMupe+AbDQZn2LNwYDoaZZDvs+7YqcPH1dil5qjbb8GuuEdw93nB4VudF95u9GKGL841OuPAsMt2FfMKnqlmbIadIp3lwgk1eTrrfykCksGS4S2lL9uixX6V2tF9zXW/fLmFIJ7xHtjgofhZsJQown2pQrNnxBibWk2lDd5fpTKooPsHp6CPBlUzTtacaCvjqV/vOgtUiql74hL2Mbq9rXCMykkmaIpLt0NbStwir/1oo3G2wuTDiMQKBgQDITFywS/sZ4vA5hz4NkzlFS0M7VoVZ3oysfPnNzyU6J2uE1+VKyTM1ncJegOScriYo238Gnbu30Jq1kY2iNFBDqveSgErkhNF8b1pdBqknRIOgHcf9Kz96L5K6Pu3gZFnWXC+qbM47cLIfk55es/LvN7kQGNH5fVaqjFfsbu2yJQKBgQDG+6mOK47vU51dMlzT/LBkeD04RL83sK6dxkCYbG8cLf+bcdlLjcXl+E/PUW6bxUIgCm+ib73mBZ3K2TAkNjA9f83mzpcpIbM3WctX/FNh27rjDu+Wswd/6tzMyuoey4EASMAmFlZyrdhJqNuuhD3SRfLK77yemAq2PmndZEOVCwKBgH5Jr1M0xOCAdqg+/j/+6GgpWP2Lws50BEwpDDPYfIdbHW6H1Tk+/Hu8uTVunTWwk7zFECUyxI3UCAec+ykfRNA1dp03KIFGwPJtHxNyRKrOhxMoU9TrNL2sSx4E2WTWwNHoE+GncqyFlLlWEM9zNCPiBVwB2jos7bzgeftHwbTFAoGBAMbwANrk7aiU3jW5DlnavrgUBpDlGpAhEtMmzJoXfxabXnwY3PjOq1Z6ZcCOV5lhI/VIucebFC6O2u1dKuZpTt2Nk1v4m+RBjx39pnE3El46AqTT3/G41/yp4UrWbC+Rok2YbpMlrhRFfoJWUhwulmhOCqmd+eRNehguWkU/4tl1AoGAOPrbWPkU7qGrA6KWJ5BspjTECflVh304nRhxTO+kprdHN0/HbEZkJrsV+igzftsM7RWwdJUqK9kkJ7YdLsFGbZFlCdcdcJ4rUjY+1IFobSKu1QG0EHlsiu26l1rc8hKxxdTC6o71d6D7KVyzE1/pFBxFa6HnB9c7wCoSi4Gq/ZA="
    #
    # payment_method = "ANZ"
    # amount = 20000
    # cash_account = "1231234353"
    pay_out_request_demo(env, merchant_id, merchant_secret, private_key, payment_method, amount, cash_account)
