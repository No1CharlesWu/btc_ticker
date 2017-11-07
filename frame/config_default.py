configs = {
    'db': {
        'host': '127.0.0.1',
        'port': 27017,
        'user': 'root',
        'password': "'",
        'database': 'crawler'
    },
    'task': {
        'okcoin.cn': {
            'rest': {
                'btc': {
                    'ticker',
                    'depth_0.01',
                    'depth_0.1',
                    'depth_1',
                    'trades',
                    'kline_1min',
                    'kline_3min'
                },
                'ltc': {
                    'ticker',
                    'depth_0.01',
                    'depth_0.1',
                    'depth_1',
                    'trades',
                    'kline_1min',
                    'kline_3min'
                }
            }
        },
        'okcoin.com': {
            'rest': {
                'btc': {
                    'ticker',
                    'depth_0.01',
                    'depth_0.1',
                    'depth_1',
                    'trades',
                    'kline_1min',
                    'kline_3min'
                },
                'ltc': {
                    'ticker',
                    'depth_0.01',
                    'depth_0.1',
                    'depth_1',
                    'trades',
                    'kline_1min',
                    'kline_3min'
                }
            }
        },
        'huobi.com': {
            'rest': {
                'btc_cny': {
                    'ticker',
                    'depth',
                    'detail',
                    'kline_1min',
                    'kline_5min'
                },
                'ltc_cny': {
                    'ticker',
                    'depth',
                    'detail',
                    'kline_1min',
                    'kline_5min'
                },
                'btc_usd': {
                    'ticker',
                    'depth',
                    'detail',
                    'kline_1min',
                    'kline_5min'
                }
            }
        }
    }
}
