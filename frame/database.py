from pymongo import MongoClient
import pymongo

"""
DataBase 数据库初始化、查询、插入等基本操作
"""


class DataBase(object):
    def __init__(self, d_db):
        """
        初始化并连接数据库
        :param d_db: 根据参数连接数据库 dict
        """
        # TODO: 未做异常处理
        self.client = MongoClient(host=d_db['host'], port=d_db['port'])
        self.database = self.client[d_db['database']]

    def get_db(self):
        """
        :return: 数据库句柄
        """
        return self.database

    def get_collection(self, collection_name):
        """
        :param collection_name: 集合名（表名） str
        :return: 集合（表）句柄
        """
        return self.database[collection_name]

    def find(self, collection_name):
        """
        查询集合（表）全部内容
        :param collection_name: 集合名（表名） str
        :return: 集合（表）的游标 list
        """
        coll = self.database[collection_name]
        return coll.find()

    def find_last_one(self, collection_name):
        """
        查询集合（表）最近时间的一条数据
        :param collection_name: 集合名（表名） str
        :return: 最近时间一条数据 dict
        """
        coll = self.database[collection_name]
        # return coll.find().sort({'time': -1}).limit(1)
        return coll.find().sort('timestamp', -1).limit(1)

    def insert(self, collection_name, data):
        """
        插入数据
        :param collection_name: 集合名（表名） str
        :param data: 一条或多条数据 dict/list
        :return: 无
        """
        # TODO 插入失败等处理
        coll = self.database[collection_name]
        if isinstance(data, dict):
            result = coll.insert_one(data)
        elif isinstance(data, list):
            result = coll.insert_many(data)
        else:
            print('data error')

    def create_index(self, collection_name, data):
        """
        插入索引
        :param collection_name: 集合名（表名） str
        :param data: 格式 list [('timestamp','ASCENDING')] [('timestamp','DESCENDING')]
        :return: 无
        """
        # TODO 感觉接口写的不好
        l = list()
        for i_d in data:
            t = tuple()
            if i_d[1] == 'ASCENDING':
                t = (i_d[0], pymongo.ASCENDING)
            elif i_d[1] == 'DESCENDING':
                t = (i_d[0], pymongo.DESCENDING)
            l.append(t)
        coll = self.database[collection_name]
        coll.create_index(l)

    def update(self):
        pass

    def remove(self):
        pass


if __name__ == '__main__':
    configs = {
        'db': {
            'host': '127.0.0.1',
            'port': 27017,
            'user': 'root',
            'password': "'",
            'database': 'btc_ticker'
        }
    }
    s = 'okcoincom_rest_btc_ticker'
    a = DataBase(configs['db'])
    # c = a.find_one(s)
    col = a.get_collection(s)
    print(col)
    c = a.find(s)
    c = a.find_last_one(s)
    print(c)
    for i in c:
        print(i)

        # for i in range(10000):
        #     data = {'time': i, 'buy': 100, 'sell': 200}
        #     a.create_index('okcoincn_rest_btc_ticker', [('timestamp', 'DESCENDING')])
        #     a.insert('okcoincn_rest_btc_ticker', data)
