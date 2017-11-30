import copy
import time
import requests
import http.client
import json
import hashlib
from frame import taskbase
from library import okcoin_spot_api
from task import write_json



class Task(taskbase.TaskBase):
    def do(self):
        print(self.module_name)
        # 设置下次添加此任务的间隔时间，若不设置，则self.loop = False self.interval = -1 为不再添加此项任务
        self.set_interval(1)

        # 初始化api_key，secret_key,url
        # api_key = 'c9c41a5d-b67a-4cb2-9cbd-c34cd19ad6c4'
        # secret_key = 'EECA1AA8FB0A5BA6A1123D21A10A9944'
        # okcoin_rest_url = 'www.okex.com'

        # 初始化url
        bitfinex_url = "https://api.bitfinex.com/v1/pubticker/btcusd"
        # 现货API
        try:
            response = requests.request("GET", bitfinex_url)
            if response.status_code == 200:
                self.data = json.loads(response.text)
            elif response.status_code == 400:
                print("bad request")
                return
            else:
                print("unknown response.status_code == %d" %response.status_code)
                return
        except Exception as e:
            print('Exception bitfinex_ticker:', e)
            return

        # print(self.data)
        # print(type(self.data))
        # print(self.data['bid'])

    def do_after(self):
        if self.data == None:
            return
        else:
            self.result = self.data_filter(self.data)
            write_json.all_dict[self.module_name] = copy.deepcopy(self.result)
            self.data_insert()


    def data_filter(self, data):
        r = dict()
        r['timestamp'] = int(float(data['timestamp']) * 1000)
        r['buy'] = float(data['bid'])
        r['high'] = float(data['high'])
        r['last'] = float(data['last_price'])
        r['low'] = float(data['low'])
        r['mid'] = float(data['mid'])
        r['sell'] = float(data['ask'])
        r['vol'] = float(data['volume'])
        return r

    def data_insert(self):
        self.db.create_index(self.module_name, [('timestamp', 'DESCENDING')])
        self.db.insert(self.module_name, self.result)


if __name__ == '__main__':
    a = Task('a',None)
