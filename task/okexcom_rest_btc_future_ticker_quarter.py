import copy
import time
from frame import taskbase
from library import okcoin_spot_api
from task import write_json


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
        print(self.module_name)
        # 设置下次添加此任务的间隔时间，若不设置，则self.loop = False self.interval = -1 为不再添加此项任务
        self.set_interval(1)

        # 初始化api_key，secret_key,url
        api_key = 'c9c41a5d-b67a-4cb2-9cbd-c34cd19ad6c4'
        secret_key = 'EECA1AA8FB0A5BA6A1123D21A10A9944'
        okcoin_rest_url = 'www.okex.com'

        # 现货API
        okcoin_spot = okcoin_spot_api.OKCoinSpot(okcoin_rest_url, api_key, secret_key)

        try:
            self.data = okcoin_spot.future_ticker(symbol='btc_usd',contract_type='quarter')
        except Exception as e:
            print('Exception rest_ticker:', e)
            return

    def do_after(self):
        if self.data == None:
            return
        else:
            self.result = self.data_filter(self.data)
            write_json.all_dict[self.module_name] = copy.deepcopy(self.result)
            # self.data_insert()

    def data_filter(self, data):
        r = dict()
        r['timestamp'] = int(data['date']) * 1000
        r['buy'] = float(data['ticker']['buy'])
        r['high'] = float(data['ticker']['high'])
        r['last'] = float(data['ticker']['last'])
        r['low'] = float(data['ticker']['low'])
        r['sell'] = float(data['ticker']['sell'])
        r['vol'] = float(data['ticker']['vol'])
        r['contract_id'] = str(data['ticker']['contract_id'])
        r['unit_amount'] = float(data['ticker']['unit_amount'])
        return r

    def data_insert(self):
        self.db.create_index(self.module_name, [('timestamp', 'DESCENDING')])
        self.db.insert(self.module_name, self.result)


if __name__ == '__main__':
    pass
