import time
from frame import taskbase
from library import okcoin_spot_api

okcoincn_rest_ltc_kline_1min_last_timestamp = 0


class Task(taskbase.TaskBase):
    def do(self):
        """
        1417536000000,	时间戳
        2370.16,	开
        2380,		高
        2352,		低
        2367.37,	收
        17259.83	交易量
        symbol  String  是   btc_cny：比特币， ltc_cny：莱特币
        type    String  是  1min : 1分钟  3min : 3分钟  5min : 5分钟  15min : 15分钟    30min : 30分钟
                            1day : 1日   3day : 3日   1week : 1周  1hour : 1小时     2hour : 2小时
                            4hour : 4小时 6hour : 6小时 12hour : 12小时
        size    Integer 否(默认全部获取)   指定获取数据的条数
        since   Long    否(默认全部获取)   时间戳（eg：1417536000000）。 返回该时间戳以后的数据
        :return:
        """
        print('okcoincn_rest_ltc_kline_1min')
        # 设置下次添加此任务的间隔时间，若不设置，则self.loop = False self.interval = -1 为不再添加此项任务
        self.set_interval(60)

        # 初始化api_key，secret_key,url
        api_key = 'c3b622bc-8255-40f2-9585-138928ae376d'
        secret_key = '7C1DDC1745C93B87BE1643A689938459'
        okcoin_rest_url = 'www.okcoin.cn'

        # 现货API
        okcoin_spot = okcoin_spot_api.OKCoinSpot(okcoin_rest_url, api_key, secret_key)

        try:
            data = okcoin_spot.kline(symbol='ltc_cny', type='1min', size=5,
                                     since=okcoincn_rest_ltc_kline_1min_last_timestamp)
        except Exception as e:
            print('Exception rest_kline_1min:', e)
            return

        # print(time.strftime("%H:%M:%S"), data, type(data))
        self.result = self.data_filter(data)
        # print(self.result)
        if self.result:
            self.data_insert()

    def data_filter(self, data):
        r = list()
        for i in range(len(data)):
            temp_d = {'timestamp': data[i][0], 'open': data[i][1], 'high': data[i][2], 'low': data[i][3],
                      'close': data[i][4], 'vol': data[i][5]}
            r.append(temp_d)
            global okcoincn_rest_ltc_kline_1min_last_timestamp
            okcoincn_rest_ltc_kline_1min_last_timestamp = data[i][0]
        r.pop()
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
