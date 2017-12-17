configs = {
    'db': {
        'host': '127.0.0.1',
        'port': 27017,
        'user': 'root',
        'password': "'",
        'database': 'btc_ticker'
    },
    'task': {
        'okcoin.com': {
            'rest': {
                'btc': {
                    'ticker'
                }
            }
        },
        'okex.com':{
            'rest':{
                'btc':{
                    'future_ticker_this_week',
                    'future_ticker_next_week',
                    'future_ticker_quarter',
                    'ticker'
                }
            }
        },
        'bitfinex.com':{
            'rest':{
                'btc':{
                    'ticker'
                }
            }
        },
        'bitmex.com':{
            'rest':{
                'btc':{
                    'XBTUSD'
                    'XBTZ17'
                }
            }
        },
        'write':{
            'json'
        }
    }
}
