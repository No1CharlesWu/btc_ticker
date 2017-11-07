# coding=utf-8
from library.huobi_util import *


def getAccountInfo(method):
    """
    获取账号详情
    :param method:
    :return:
    """
    params = {"method": method}
    extra = {}
    res = send2api(params, extra)
    return res


def getOrders(coinType, method):
    """
    获取所有正在进行的委托
    :param coinType:
    :param method:
    :return:
    """
    params = {"method": method}
    params['coin_type'] = coinType
    extra = {}
    res = send2api(params, extra)
    return res


def getOrderInfo(coinType, id, method):
    """
    获取订单详情
    :param coinType:
    :param id:
    :param method:
    :return:
    """
    params = {"method": method}
    params['coin_type'] = coinType
    params['id'] = id
    extra = {}
    res = send2api(params, extra)
    return res


def buy(coinType, price, amount, tradePassword, tradeid, method):
    """
    限价买入
    :param coinType:
    :param price:
    :param amount:
    :param tradePassword:
    :param tradeid:
    :param method:
    :return:
    """
    params = {"method": method}
    params['coin_type'] = coinType
    params['price'] = price
    params['amount'] = amount
    extra = {}
    extra['trade_password'] = tradePassword
    extra['trade_id'] = tradeid
    res = send2api(params, extra)
    return res


def sell(coinType, price, amount, tradePassword, tradeid, method):
    """
    限价卖出
    :param coinType:
    :param price:
    :param amount:
    :param tradePassword:
    :param tradeid:
    :param method:
    :return:
    """
    params = {"method": method}
    params['coin_type'] = coinType
    params['price'] = price
    params['amount'] = amount
    extra = {}
    extra['trade_password'] = tradePassword
    extra['trade_id'] = tradeid
    res = send2api(params, extra)
    return res


def buyMarket(coinType, amount, tradePassword, tradeid, method):
    """
    市价买
    :param coinType:
    :param amount:
    :param tradePassword:
    :param tradeid:
    :param method:
    :return:
    """
    params = {"method": method}
    params['coin_type'] = coinType
    params['amount'] = amount
    extra = {}
    extra['trade_password'] = tradePassword
    extra['trade_id'] = tradeid
    res = send2api(params, extra)
    return res


def sellMarket(coinType, amount, tradePassword, tradeid, method):
    """
    市价卖出
    :param coinType:
    :param amount:
    :param tradePassword:
    :param tradeid:
    :param method:
    :return:
    """
    params = {"method": method}
    params['coin_type'] = coinType
    params['amount'] = amount
    extra = {}
    extra['trade_password'] = tradePassword
    extra['trade_id'] = tradeid
    res = send2api(params, extra)
    return res


def getNewDealOrders(coinType, method):
    """
    查询个人最新10条成交订单
    :param coinType:
    :param method:
    :return:
    """
    params = {"method": method}
    params['coin_type'] = coinType
    extra = {}
    res = send2api(params, extra)
    return res


def getOrderIdByTradeId(coinType, tradeid, method):
    """
    根据trade_id查询oder_id
    :param coinType:
    :param tradeid:
    :param method:
    :return:
    """
    params = {"method": method}
    params['coin_type'] = coinType
    params['trade_id'] = tradeid
    extra = {}
    res = send2api(params, extra)
    return res


def cancelOrder(coinType, id, method):
    """
    撤销订单
    :param coinType:
    :param id:
    :param method:
    :return:
    """
    params = {"method": method}
    params['coin_type'] = coinType
    params['id'] = id
    extra = {}
    res = send2api(params, extra)
    return res
