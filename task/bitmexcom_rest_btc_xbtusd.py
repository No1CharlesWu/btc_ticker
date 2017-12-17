import copy
import time
import requests
import http.client
import json
import hashlib
from frame import taskbase
from task import write_json
from library.BitMEXAPIKeyAuthenticator import APIKeyAuthenticator
from bravado.client import SwaggerClient
from bravado.requests_client import RequestsClient


class Task(taskbase.TaskBase):
    def do(self):
        print(self.module_name)
        # 设置下次添加此任务的间隔时间，若不设置，则self.loop = False self.interval = -1 为不再添加此项任务
        self.set_interval(1)

        # 初始化api_key，secret_key,url
        API_KEY = 'SwcHA0YKoYai55_aDRnwP6v9'
        API_SECRET = 'ere_BrBO7BLNHK290zAPLzhBhII2zUrsWM3gG0R3MbJgtXxp'
        HOST = "https://www.bitmex.com"
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
            request_client = RequestsClient()
            request_client.authenticator = APIKeyAuthenticator(HOST, API_KEY.encode('utf-8'), API_SECRET.encode('utf-8'))

            bitmex_basic_request = SwaggerClient.from_url(SWAGGER_URI, config=config)
            # bitmex_authenticated_request = SwaggerClient.from_url(SWAGGER_URI, config=config,http_client=request_client)

            response_orderbook = bitmex_basic_request.OrderBook.OrderBook_get(symbol='XBTUSD', depth=1).result()
            response_stats = bitmex_basic_request.Stats.Stats_get().result()

            self.data = self.getData(response_orderbook, response_stats)
        except Exception as e:
            print('Exception bitfinex_ticker:', e)
            return

    def getData(self, orderbook, stats):
        r = dict()
        for d in orderbook:
            if d['symbol'] == 'XBTUSD':
                r['buy'] = d['bidPrice']
                r['sell'] = d['askPrice']
                r['timestamp'] = d['timestamp'].timestamp()*1000
        for d in stats:
            if d['rootSymbol'] == 'XBT':
                r['vol'] = d['turnover24h']
        return r

    def do_after(self):
        if self.data == None:
            return
        else:
            self.result = self.data_filter(self.data)
            print(self.result)
            write_json.all_dict[self.module_name] = copy.deepcopy(self.result)
            self.data_insert()

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
