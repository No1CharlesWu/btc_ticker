import datetime

from library import huobi_api
from frame import taskbase

class Task(taskbase.TaskBase):
    def do(self):
        print('huobicom_rest_ltc_cny_ticker')
        # 设置下次添加此任务的间隔时间，若不设置，则self.loop = False self.interval = -1 为不再添加此项任务
        self.set_interval(1)

        huobi_spot = huobi_api.HuobiSpot(huobi_api.API_KEY, huobi_api.SECRET_KEY)

        try:
            data = huobi_spot.get_ticker(huobi_api.TICKER_LTC_CNY)
        except Exception as e:
            print('Exception rest_ticker:', e)
            return

        # print(type(data), data)
        self.result = self.data_filter(data)
        # print(self.result)
        if self.result:
            self.data_insert()

    def data_filter(self, data):
        r = data['ticker']
        r['time'] = int(data['time']) * 1000
        r['timestamp'] = int(datetime.datetime.now().timestamp() * 1000)
        return r

    def data_insert(self):
        self.db.create_index(self.module_name, [('timestamp', 'DESCENDING')])
        self.db.insert(self.module_name, self.result)

if __name__ == '__main__':
    import time

    task = Task('a', 'b')
    j = 1
    for i in range(360):
        time.sleep(5)
        print(j)
        j += 1
        task.do()