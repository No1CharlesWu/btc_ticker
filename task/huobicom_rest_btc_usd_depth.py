import datetime

from library import huobi_api
from frame import taskbase

huobicom_rest_btc_usd_depth_last_id = 0


class Task(taskbase.TaskBase):
    def do(self):
        print('huobicom_rest_btc_usd_depth')
        # 设置下次添加此任务的间隔时间，若不设置，则self.loop = False self.interval = -1 为不再添加此项任务
        self.set_interval(1)

        huobi_spot = huobi_api.HuobiSpot(huobi_api.API_KEY, huobi_api.SECRET_KEY)

        try:
            data = huobi_spot.get_depth(huobi_api.DEPTH_BTC_USD, 20)
        except Exception as e:
            print('Exception rest_depth:', e)
            return

        # print(type(data), data)
        self.result = self.data_filter(data)
        # print(self.result)
        if self.result:
            self.data_insert()

    def data_filter(self, data):
        global huobicom_rest_btc_usd_depth_last_id
        if huobicom_rest_btc_usd_depth_last_id == data['id']:
            return None
        else:
            huobicom_rest_btc_usd_depth_last_id = data['id']
            data['timestamp'] = data['ts']
            data.pop('ts')
            return data

    def data_insert(self):
        self.db.create_index(self.module_name, [('timestamp', 'DESCENDING')])
        self.db.insert(self.module_name, self.result)


if __name__ == '__main__':
    import time

    task = Task('a', 'b')
    j = 1
    for i in range(360):
        time.sleep(1)
        print(j)
        j += 1
        task.do()
