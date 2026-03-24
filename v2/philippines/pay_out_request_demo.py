import json

import requests

from v2.philippines import Tool_Sign
from v2.philippines.bean.AreaEnum import AreaEnum
from v2.philippines.bean.AreaEnum import CurrencyEnum
from v2.philippines.bean.Constants import Constants
from v2.philippines.bean.MerchantReq import MerchantReq
from v2.philippines.bean.MoneyReq import MoneyReq
from v2.philippines.bean.ReceiverReq import ReceiverReq
from v2.philippines.bean.TradePayoutReq import TradePayoutReq


def pay_out_request_demo(env, merchant_id, merchant_secret, private_key, payment_method, amount, cash_account,
                         receiverName):
    global request_path
    if env == "production":
        # production
        request_path = Constants.baseUrl + "/v2.0/disbursement/pay-out"
    if env == "sandbox":
        # sandbox
        request_path = Constants.baseUrlSandbox + "/v2.0/disbursement/pay-out"

    # transaction time
    timestamp = Tool_Sign.get_formatted_datetime('America/Sao_Paulo')
    print("timestamp:" + timestamp)
    # partner_id
    merchant_order_no = merchant_id + Tool_Sign.generate_32bit_uuid()
    purpose = "Purpose For Transaction from python SDK"

    # moneyReq
    money_req = MoneyReq(CurrencyEnum.PHP.name, amount)
    # merchantReq
    merchant_req = MerchantReq(merchant_id, "your merchant name", None)

    # receiverReq
    receiver_req = ReceiverReq(receiverName, None, None)

    # payInReq
    pay_in_req = TradePayoutReq(payment_method, None, receiver_req, cash_account, merchant_order_no[:32], purpose,
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


# run
if __name__ == '__main__':
    env = 'production'
    # merchant_id = '20158'
    # merchant_secret = 'ebef0a7119b5208e84633f63dafd61110ae97e24ee4d120bb04045aa28111671'
    # private_key = 'MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCEGyBGscdvb86+tKjGqVUdXv1NqVXz9H4PLdAZsdvW+rHKbr9SEFddDOi2qUiICIHyip3Y4qHKYVB4KcI5ZqknHpWh3dB32Khj4TMqM6YXe7BGaUeYoncjCBfFDDysX+a629cIFX4Fnu6VqbKkRJzRiwqQg7uhFwXhvtrHQfEGTo4Co2wC6B4MGLDEYZwDbBYRpGhLPQ9kDejuvdBLw50QY52ah3SpDC/oy9n8lT+BgL6bNod0xA6W2BuR63wwo1knz3uNDRwSReKvHtoGF58j/8oSk1cmctttWV6QIYyriynLDMRUVAst+JvgugJG6ae44MteullloPkXNdhUWCF7AgMBAAECggEAFzitc7/MTspYjS00fbdGPuNzozMg6MERZ5ml+t5IxoFKv0q4VrSIptKeFX2sQj08mmXDWVx9FBYHDxhIC87/7OBzbQCQpIBxGR184O4zQ+16DuZyr2Hfj0jc5MZB5Ar3g+Eg60rb3CETzzsFK9rjtfG66aw+TxK89fGWg3AT7gegRx35w01e1geLm0yPs1LS/aqj952jfUVdzTMMDRi7qccKoZ9QzCLcaKgFJFthIts2nq+bM2UixSVP/veQZoaLOBKXtPT6grviClebIrw0ocXOWfXwwDSL/ROu1j/0A8d9+PWoKhyIE2bZQhFoAsYEIrC86yeh6e5uqL6vMxjAAQKBgQC5pfrntQYKTA6VACm2touC89cnujOwoI46xLxPsbRF8Z2mETlLbGENiX+Xkd8p/glZJbe2FHdmKAaoQAsSyChJoH/840xRcUY4TIUkQhaNBpWxfiRynFspUb4LMpqg6sygjswj3Gt67fjC2fYJuvzNDEvE0/wKltvrmyZu4oXG2wKBgQC2KutXedBAeX9nysrZ7NI2TjW/zigOhW9vLHnUgnyoIY7CAq8sib4k9fR8c/Gx/0flmDOTcVvPUMWaVfmrlXtgoD9/6uS25uarq0ZjZwqBzeTCimHazYfHwrmjgAr1oCINffMXOqYGpsdjfrTQRqK+v1F6i1p2PVb+v1G5Z7CB4QKBgCM2r4vp01Z6rL1ohYEJyRayx9naQNm86p2NGacILwihVuTcGYEL8rDNpu0KF0lwzTcip2EbKrau2uxpEXCjlLi6f+xo9N3x3X7qTMre2kYvvI8pPSKcM9J3ldOr6pahUuUVkPUwZxavMuNK0pdv52nBblHMX99mVBqxmC2qO/PHAoGAJaTy4y3KCjjRSjqO9r/IpO4+jzdj8bRDVd8EAhVA+2GL5a22U2bXgz3MWxd+n8DYM6rjJZnsVggj/YO8x2dpiosy9BUvVFic3GbVcd8uPaq1ljoQhK2qXG5x/EaOfTmtL8qSPH+jJYa7d2UMqmmeYfqZNNCtTffZDWWt1rmFsSECgYEApRmch1TBZKNO/zfTQkE133sQXFx4MyUZEP/0i9kYUIHdCzYCfKhFBcUuuED588VMqZKApZbI7BaxSddBrr73vq4rt9kNzVnPuCHpY9Y086WLOnIPqngUgDq39gAq7awyPBvin5pdRVoXJm2iOOjJOBCP/zDfQybaIuyx6ZMISIs='

    # merchant_id = '20190'
    # merchant_secret = '8decca074fa734af3b74bf3ee2de50bdce56f715cbc7e3788b59b72d8fb4776d'
    # private_key = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCbr/c44T8qWI2k6i+yZFJfFhhhnEu9Fu69g5o9UgKui8W/+18pCt9LEgSjQGgxFJe6C8X18kAXoxfstIkkSnL7q55/rXyNkymOmwpRXoO8ApgCNIlSHISKgUhaDm5pZvFvNn2u9Rsyhv9HYlf4D+e+1MkoD1dRQeefoO9nQTE5fA4uqpiKBvu7q9FJyUMI8+57ZWOddReWhLWpEkNlyDglAzdSy+wObIBx0hgKRdPWgOpuSDsSnjoAdb1+dA2PKjicAcwJOJKVAohiT70xJHnnAYFVn4w8SzkordhqV6R4XDzhnJMWr8FCPHYFvypfDKz2ZLn4pzXxVRWkPHYwlTCXAgMBAAECggEARzljYpQ5r4e/lTjGBVi8DmAvW0iDpcf+BJlWUMNaErxDBadcS4x7xv5BPOZURE/lcem88N2Y0Ld+VH3rV7zviY9j/YlCuAohMupe+AbDQZn2LNwYDoaZZDvs+7YqcPH1dil5qjbb8GuuEdw93nB4VudF95u9GKGL841OuPAsMt2FfMKnqlmbIadIp3lwgk1eTrrfykCksGS4S2lL9uixX6V2tF9zXW/fLmFIJ7xHtjgofhZsJQown2pQrNnxBibWk2lDd5fpTKooPsHp6CPBlUzTtacaCvjqV/vOgtUiql74hL2Mbq9rXCMykkmaIpLt0NbStwir/1oo3G2wuTDiMQKBgQDITFywS/sZ4vA5hz4NkzlFS0M7VoVZ3oysfPnNzyU6J2uE1+VKyTM1ncJegOScriYo238Gnbu30Jq1kY2iNFBDqveSgErkhNF8b1pdBqknRIOgHcf9Kz96L5K6Pu3gZFnWXC+qbM47cLIfk55es/LvN7kQGNH5fVaqjFfsbu2yJQKBgQDG+6mOK47vU51dMlzT/LBkeD04RL83sK6dxkCYbG8cLf+bcdlLjcXl+E/PUW6bxUIgCm+ib73mBZ3K2TAkNjA9f83mzpcpIbM3WctX/FNh27rjDu+Wswd/6tzMyuoey4EASMAmFlZyrdhJqNuuhD3SRfLK77yemAq2PmndZEOVCwKBgH5Jr1M0xOCAdqg+/j/+6GgpWP2Lws50BEwpDDPYfIdbHW6H1Tk+/Hu8uTVunTWwk7zFECUyxI3UCAec+ykfRNA1dp03KIFGwPJtHxNyRKrOhxMoU9TrNL2sSx4E2WTWwNHoE+GncqyFlLlWEM9zNCPiBVwB2jos7bzgeftHwbTFAoGBAMbwANrk7aiU3jW5DlnavrgUBpDlGpAhEtMmzJoXfxabXnwY3PjOq1Z6ZcCOV5lhI/VIucebFC6O2u1dKuZpTt2Nk1v4m+RBjx39pnE3El46AqTT3/G41/yp4UrWbC+Rok2YbpMlrhRFfoJWUhwulmhOCqmd+eRNehguWkU/4tl1AoGAOPrbWPkU7qGrA6KWJ5BspjTECflVh304nRhxTO+kprdHN0/HbEZkJrsV+igzftsM7RWwdJUqK9kkJ7YdLsFGbZFlCdcdcJ4rUjY+1IFobSKu1QG0EHlsiu26l1rc8hKxxdTC6o71d6D7KVyzE1/pFBxFa6HnB9c7wCoSi4Gq/ZA="
    merchant_id = '20011'
    merchant_secret = 'b3114906e3c334ffb690f3234c8083967301d5e5d9124e3671d5219235091962'
    private_key = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDInnfRIS818CCErcTrYFxfpkYS/AVa5vYd/sYgP4C3iYotS5xVtWp6DBn5ZEIsqcRf7frJDaQ2ZvJXwDsSSDEptyAaMfTcuD7S4aNL9aEnaA5ZGF0wyGNJCTgRbOLwmuA3pvfYpgliT5uQa0dfLxX9WEaDT3M8jDu/pdagsu74dRxvmHDSKSSx8NTR86V5ycHjN8AtSief1xO6xGl/ZjS5GQ/GQbxZ4TYVlYzbCe9/KpVI14+I6JIUO7yRMQGUNcJKoxTXuemssXSVSsUV1J2eSr6qCeO88np+58PqygpiuxhlXxzO+mYXal3sBclZKhzU9fvuGW5mb42NCpFh98kDAgMBAAECggEADvpMbg0WW2ZfjyLyt4icrOQa3tz462CgkacNP1LDtzAqDu1SW9BtBXVKKnqH5Dy9H/+s6v4SkKCJSZrc7iWnTKV9hzx2kFSjFWxqHB2CWBD74pP1P9NIx6b2ts+py8EhqetUcqocEOkU71MgY3n+SslLOQ92m4J0DYAB8O0a9pU/GTSppGikAm1aUAZSFuZDg1uxyt4vy4dfB3JK72XUFEC0asOA6KRnpUXLx0L5tJJPC79OV3/yAQ6CUQYY/vnZBWF8ihbDhpRTBgea1qXcDecVte1ueo/FvXfWDBo6RRgH+Dw085bHRQ/2d5lJDq1dFN8luJnZia6aUeYW/1kShQKBgQD1+ineDVe07WZqiZck8XUZINZyAUB/Uqj2t3+YLFF+A47kHPgb+nOieeKsWD3JrXD0IEDGJFMMGRLo4qf8Nj4Df/9nKF/xgjMNQ9lBCobbzEEMhBLCBB1rNRPJjZ4VE+N2RqmsioZf6RIvyQKG6USeNa8FJ4c1mdx40iuztX/OtQKBgQDQyyoTOQ+/ORXLrTrlpBGYsLO4nd9vKffECn+dnvoOoYv79FsF5RWKGkIzPJ8DdYQ/Lwp/5DdEIDGSOdhz23pC365QBpKlGu+c8BNEAceTs+2nhsLijY7a0JqiBb7kZmow5CSjUU/wP87Bp19qYLODnYMwlilT3XVRlqJM8nrT1wKBgDReg4VsL80scg6ippRN+BFWhXGWRKYW8jQ80ySR4vPCTCzS4hwK0Y25B4KL8vO6Qn8nUsMcvrWnrPf6Maun3MIgAT90QCEKCFZ9qIaJeDbZoMvKXrgB6kWF8mWKCisQpe/rkXpTr9JBrAaSdEBG774DTfT5+nZ2AJOUo4tKTCC1AoGBAIIZVcpMj+dTJqWW91AH/37o+9NZa9PUjrH06LfKS326Y4NHK0BtEhLPcdiDOYHqQ9Eq+pveFCG6/ahjqt/mLjRlNDRhJBcExbFAVoDVqwn532e3rM+F7TGjMfcrJVskBZ8ZSUsKa4kD+UzpgabDQpgMGaa4ql+7alLATbksjiRZAoGAMuamEMtI1gxcQMQk0/oOEqZqsJARN/RlLZjNGwNR7UKL5znzoTGqUO8TgBIEFEJIq6rFz4d/IDuGQXLEVPAD7EFOfop1DJJ2V3kGS3i/ePK2aJ9bXOYfaLwjlQS1M3mrZQONsx9rBqvtLnpaApZ3V5T66F78V6dcBWzOEGW5uyE="

    # payment_method = "GCASH"
    payment_method = "GCASH"
    amount = 100
    cash_account = "09274345464"
    receiverName = "test"
    pay_out_request_demo(env, merchant_id, merchant_secret, private_key, payment_method, amount, cash_account, receiverName)
