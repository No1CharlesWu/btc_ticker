import time
import json
from frame import taskbase
import random

all_dict = dict()

class Task(taskbase.TaskBase):
    def do(self):
        print('write_json')
        # 设置下次添加此任务的间隔时间，若不设置，则self.loop = False self.interval = -1 为不再添加此项任务
        self.set_interval(2)
        # a = random.randint(1,100)
        # print(a)
        # test_dict = {'bigberg': [a, {1: [['iPhone', 6300], ['Bike', 800], ['shirt', 300]]}]}
        # print(test_dict)
        # print(type(test_dict))
        # dumps 将数据转换成字符串
        print(all_dict)
        # json_str = json.dumps(all_dict)
        # print(json_str)
        # print(type(json_str))
        #
        with open("/Users/charles/Sites/test.json","w") as f:
            a = all_dict
            json.dump(a,f)
            print("加载入文件完成...")

if __name__ == '__main__':
    while(1):
        a = Task('write_for_json', None)
        time.sleep(1)

