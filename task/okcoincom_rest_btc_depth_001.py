import time
import datetime
from frame import taskbase
from library import okcoin_spot_api


class Task(taskbase.TaskBase):
    def do(self):
        """
        asks :卖方深度
        bids :买方深度
        symbol  String  否(默认btc_cny)    btc_cny:比特币 ltc_cny :莱特币
        size    Integer 否(默认200)        value: 1-200
        merge   Integer 否(默认 merge参数不传时返回0.01深度)    合并深度: 1, 0.1
        :return:
        """
        print('okcoincom_rest_btc_depth_001')
        # 设置下次添加此任务的间隔时间，若不设置，则self.loop = False self.interval = -1 为不再添加此项任务
        self.set_interval(1)

        # 初始化api_key，secret_key,url
        api_key = '0668499e-340b-489e-979a-e7a5c57b3f15'
        secret_key = 'DDC039D1A0186B38301DBC5C4AF02032'
        okcoin_rest_url = 'www.okcoin.com'

        # 现货API
        okcoin_spot = okcoin_spot_api.OKCoinSpot(okcoin_rest_url, api_key, secret_key)
        try:
            data = okcoin_spot.depth(symbol='btc_usd', size=20)
        except Exception as e:
            print('Exception rest_depth', e)
            return

        # print(time.strftime("%H:%M:%S"), len(data), data, type(data))
        self.result = self.data_filter(data)
        self.data_insert()

    def data_filter(self, data):
        data['timestamp'] = int(datetime.datetime.now().timestamp() * 1000)
        return data

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
