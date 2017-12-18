import copy
import time
import requests
import http.client
import json
import hashlib
from frame import taskbase
from task import write_json
from datetime import datetime
import requests

class Task(taskbase.TaskBase):
    def do(self):
        print(self.module_name)
        # 设置下次添加此任务的间隔时间，若不设置，则self.loop = False self.interval = -1 为不再添加此项任务
        self.set_interval(1)

        # 初始化api_key，secret_key,url
        API_KEY = 'SwcHA0YKoYai55_aDRnwP6v9'
        API_SECRET = 'ere_BrBO7BLNHK290zAPLzhBhII2zUrsWM3gG0R3MbJgtXxp'
        HOST = "https://www.bitmex.com/api/v1"

        SWAGGER_URI = HOST + "/api/explorer/swagger.json"

        # See full config options at http://bravado.readthedocs.io/en/latest/configuration.html
        config = {
            # Don't use models (Python classes) instead of dicts for #/definitions/{models}
            'use_models': False,
            # This library has some issues with nullable fields
            'validate_responses': False,
        }

        # 现货API
        try:
            response_orderbook = requests.request("GET", "https://www.bitmex.com/api/v1/orderBook?symbol=XBTUSD&depth=1")
            if response_orderbook.status_code == 200:
                orderbook = json.loads(response_orderbook.text)
            else:
                orderbook = []
            response_stats = requests.request("GET", "https://www.bitmex.com/api/v1/stats")
            if response_orderbook.status_code == 200:
                stats = json.loads(response_stats.text)
            else:
                stats = []

            self.data = self.getData(orderbook, stats)
        except Exception as e:
            print('Exception xbtusd:', e)
            return

    def getData(self, orderbook, stats):
        r = dict()
        for d in orderbook:
            if d['symbol'] == 'XBTUSD':
                r['buy'] = d['bidPrice']
                r['sell'] = d['askPrice']
                # 格式没匹配上
                # r['timestamp'] = datetime.strptime(d['timestamp'], '%Y-%m-%dT%H:%M:%S.SSSZ')
                r['timestamp'] = int(datetime.now().timestamp()*1000)
        for d in stats:
            if d['rootSymbol'] == 'XBT':
                r['vol'] = d['turnover24h']
        return r

    def do_after(self):
        if self.data == None:
            return
        else:
            self.result = self.data_filter(self.data)
            write_json.all_dict[self.module_name] = copy.deepcopy(self.result)
            # self.data_insert()

    def data_filter(self, data):
        r = dict()
        r['timestamp'] = int(float(data['timestamp']) * 1000)
        r['buy'] = float(data['buy'])
        r['high'] = 0
        r['last'] = float(data['buy'])
        r['low'] = 0
        r['sell'] = float(data['sell'])
        r['vol'] = float(data['vol'])
        return r

    def data_insert(self):
        self.db.create_index(self.module_name, [('timestamp', 'DESCENDING')])
        self.db.insert(self.module_name, self.result)


if __name__ == '__main__':
    a = Task('a',None)
