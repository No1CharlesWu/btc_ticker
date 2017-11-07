import time
from frame import taskbase
from library import okcoin_spot_api

okcoincom_rest_ltc_trades_last_tid = 0


class Task(taskbase.TaskBase):
    def do(self):
        """
        date:交易时间
        date_ms:交易时间(ms)
        price: 交易价格
        amount: 交易数量
        tid: 交易生成ID
        type: buy/sell
        symbol  String  否   btc_cny:比特币 ltc_cny :莱特币
        since   Long    否   tid:交易记录ID（返回数据不包括当前tid值,最多返回600条数据）
        :return:
        """
        print('okcoincom_rest_ltc_trades')
        # 设置下次添加此任务的间隔时间，若不设置，则self.loop = False self.interval = -1 为不再添加此项任务
        self.set_interval(10)

        # 初始化api_key，secret_key,url
        api_key = '0668499e-340b-489e-979a-e7a5c57b3f15'
        secret_key = 'DDC039D1A0186B38301DBC5C4AF02032'
        okcoin_rest_url = 'www.okcoin.com'

        # 现货API
        okcoin_spot = okcoin_spot_api.OKCoinSpot(okcoin_rest_url, api_key, secret_key)
        try:
            data = okcoin_spot.trades(symbol='ltc_usd', since=okcoincom_rest_ltc_trades_last_tid)
        except Exception as e:
            print('Exception rest_trades', e)
            return

        # print(time.strftime("%H:%M:%S"), len(data), data, type(data))
        if data:
            self.result = self.data_filter(data)
            # print(okcoincom_rest_ltc_trades_last_tid, self.result)
            self.data_insert()

    def data_filter(self, data):
        r = list()
        for d in data:
            temp_d = dict()
            temp_d['amount'] = float(d['amount'])
            temp_d['timestamp'] = int(d['date_ms'])
            temp_d['price'] = float(d['price'])
            temp_d['tid'] = int(d['tid'])
            temp_d['type'] = d['type']
            r.append(temp_d)
            global okcoincom_rest_ltc_trades_last_tid
            okcoincom_rest_ltc_trades_last_tid = int(d['tid'])

        return r

    def data_insert(self):
        self.db.create_index(self.module_name, [('timestamp', 'DESCENDING')])
        self.db.insert(self.module_name, self.result)


if __name__ == '__main__':
    import time

    task = Task('a', 'b')
    j = 1
    for i in range(360):
        time.sleep(10)
        print(j)
        j += 1
        task.do()
