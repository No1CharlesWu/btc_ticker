import time
import json
import copy
from frame import taskbase

all_dict = dict()
all_list = list()
class Task(taskbase.TaskBase):
    def do(self):
        print('write_json')
        # 设置下次添加此任务的间隔时间，若不设置，则self.loop = False self.interval = -1 为不再添加此项任务
        self.set_interval(2)

        with open("~/Sites/test.json","w") as f:
            write_dict = copy.deepcopy(all_dict)
            for k,v in write_dict.items():
                v['type'] = k
                all_list.append(v)
            # dumps 将数据转换成字符串
            # json.dump(write_dict,f)
            json.dump(all_list, f)
            all_list.clear()
            print("加载入文件完成...")

if __name__ == '__main__':
    while(1):
        a = Task('write_for_json', None)
        time.sleep(1)

