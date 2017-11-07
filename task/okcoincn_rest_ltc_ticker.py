import time
from frame import taskbase
from library import okcoin_spot_api


class Task(taskbase.TaskBase):
    def do(self):
        """
        date: 返回数据时服务器时间
        buy: 买一价
        high: 最高价
        last: 最新成交价
        low: 最低价
        sell: 卖一价
        vol: 成交量(最近的24小时)
        symbol  String  否(默认btc_cny)   btc_cny:比特币    ltc_cny :莱特币
        :param symbol: 'btc_cny' 'ltc_cny'
        :return:
        """

        print('okcoincn_rest_ltc_ticker')
        # 设置下次添加此任务的间隔时间，若不设置，则self.loop = False self.interval = -1 为不再添加此项任务
        self.set_interval(1)

        # 初始化api_key，secret_key,url
        api_key = 'c3b622bc-8255-40f2-9585-138928ae376d'
        secret_key = '7C1DDC1745C93B87BE1643A689938459'
        okcoin_rest_url = 'www.okcoin.cn'

        # 现货API
        okcoin_spot = okcoin_spot_api.OKCoinSpot(okcoin_rest_url, api_key, secret_key)

        try:
            data = okcoin_spot.ticker('ltc_cny')
        except Exception as e:
            print('Exception rest_ticker:', e)
            return

        # print(time.strftime("%H:%M:%S"), data, type(data))
        self.result = self.data_filter(data)

        self.data_insert()

    def data_filter(self, data):
        r = dict()
        r['timestamp'] = int(data['date']) * 1000
        r['buy'] = float(data['ticker']['buy'])
        r['high'] = float(data['ticker']['high'])
        r['last'] = float(data['ticker']['last'])
        r['low'] = float(data['ticker']['low'])
        r['sell'] = float(data['ticker']['sell'])
        r['vol'] = float(data['ticker']['vol'])
        return r

    def data_insert(self):
        self.db.create_index(self.module_name, [('timestamp', 'DESCENDING')])
        self.db.insert(self.module_name, self.result)


if __name__ == '__main__':
    pass
