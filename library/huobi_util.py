# coding=utf-8
import hashlib
import time
import urllib
import urllib.parse
import urllib.request
import json

# 在此输入您的Key
ACCESS_KEY = "d9cf78de-f6da672b-52911e2c-b064c"
SECRET_KEY = "03ff8324-f6092b49-b370309f-2cff5"

HUOBI_SERVICE_API = "https://api.huobi.com/apiv3"
ACCOUNT_INFO = "get_account_info"
GET_ORDERS = "get_orders"
ORDER_INFO = "order_info"
BUY = "buy"
BUY_MARKET = "buy_market"
CANCEL_ORDER = "cancel_order"
NEW_DEAL_ORDERS = "get_new_deal_orders"
ORDER_ID_BY_TRADE_ID = "get_order_id_by_trade_id"
SELL = "sell"
SELL_MARKET = "sell_market"


def send2api(pParams, extra):
    """
    发送信息到api
    :param pParams:
    :param extra:
    :return:
    """
    pParams['access_key'] = ACCESS_KEY
    pParams['created'] = int(time.time())
    pParams['sign'] = createSign(pParams)
    if (extra):
        for k in extra:
            v = extra.get(k)
            if (v != None):
                pParams[k] = v
                # pParams.update(extra)
    tResult = httpRequest(HUOBI_SERVICE_API, pParams)
    return tResult


def createSign(params):
    """
    生成签名
    :param params:
    :return:
    """
    params['secret_key'] = SECRET_KEY
    params = sorted(params.items(), key=lambda d: d[0], reverse=False)
    message = urllib.parse.urlencode(params)
    message = message.encode(encoding='UTF8')
    m = hashlib.md5()
    m.update(message)
    m.digest()
    sig = m.hexdigest()
    return sig


def httpRequest(url, params):
    """
    request
    :param url:
    :param params:
    :return:
    """
    postdata = urllib.parse.urlencode(params)
    postdata = postdata.encode('utf-8')

    fp = urllib.request.urlopen(url, postdata)
    if fp.status != 200:
        return None
    else:
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()
        return json.loads(mystr)


def get_md5_value(src):
    """
    获得 MD5
    :param src:
    :return:
    """
    myMd5 = hashlib.md5(src.encode('utf8'))
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest
