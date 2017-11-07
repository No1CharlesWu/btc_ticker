import time
import datetime

from library import huobi_api
from frame import taskbase

huobi_rest_ltc_cny_kline_1min_last_timestamp = 0


class Task(taskbase.TaskBase):
    def do(self):
        print('huobicom_rest_ltc_kline_1min')
        # 设置下次添加此任务的间隔时间，若不设置，则self.loop = False self.interval = -1 为不再添加此项任务
        self.set_interval(60)

        huobi_spot = huobi_api.HuobiSpot(huobi_api.API_KEY, huobi_api.SECRET_KEY)

        try:
            data = huobi_spot.get_kline(huobi_api.KLINE_LTC_CNY, '001', 5)
        except Exception as e:
            print('Exception rest_kline_1min:', e)
            return

        # print(type(data), data)
        self.result = self.data_filter(data)
        # print(self.result)
        if self.result:
            self.data_insert()

    def data_filter(self, data):
        global huobi_rest_ltc_cny_kline_1min_last_timestamp
        r = list()
        for i in range(len(data) - 1):
            d = data[i][0]
            t_date = datetime.datetime(int(d[0:4]), int(d[4:6]), int(d[6:8]), int(d[8:10]), int(d[10:12]),
                                       int(d[12:17]))
            t_date = int(t_date.timestamp() * 1000)
            # print(d, t_date, huobi_rest_ltc_cny_kline_1min_last_timestamp)
            if t_date > huobi_rest_ltc_cny_kline_1min_last_timestamp:
                huobi_rest_ltc_cny_kline_1min_last_timestamp = t_date
                temp_d = {'timestamp': t_date, 'open': data[i][1], 'high': data[i][2], 'low': data[i][3],
                          'close': data[i][4], 'vol': data[i][5]}
                r.append(temp_d)
        return r

    def data_insert(self):
        self.db.create_index(self.module_name, [('timestamp', 'DESCENDING')])
        self.db.insert(self.module_name, self.result)


if __name__ == '__main__':
    # import time
    #
    # task = Task('a', 'b')
    # j = 1
    # for i in range(360):
    #     time.sleep(10)
    #     print(j)
    #     j += 1
    #     task.do()
    d = '20170611201900000'
    ad = '2017 06 11 19 16 00000'
    print(d[0:4])
    print(d[4:6])
    print(d[6:8])
    print(d[12:18])
    c = datetime.datetime(int(d[0:4]), int(d[4:6]), int(d[6:8]), int(d[8:10]), int(d[10:12]),
                          int(d[12:17]))
    print(c.timestamp())
    print(datetime.datetime.now())
    print(datetime.datetime.now().timestamp())
    print(datetime.datetime.fromtimestamp(c.timestamp()))
