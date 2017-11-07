import re
import importlib

"""
configs 中如果出现了不符合函数命名规则的字符，则删去。例如：okcoin.cn' 变为 'okcoincn'
Config类读取 config_default.py 和 config_override.py 对配置文件内容读入，
把task变成一个list，其中存放需要进行的任务函数名称，db 是配置数据库的信息。
"""


class Config(object):
    """
    用于读取config的配置文件进行配置。
    """

    def __init__(self):
        """
        重读配置文件，合并config_default.py 和 config_override.py。
        db : mongodb的配置
        task : 具体任务模块
        """
        try:
            from frame import config_default
            importlib.reload(config_default)
            self.configs = config_default.configs
        except ImportError:
            print('Error: %s' % ImportError)
            print('can not find config_default.py')

        try:
            from frame import config_override
            importlib.reload(config_override)
            self.configs = self.merge(self.configs, config_override.configs)
        except ImportError:
            pass

        self.db = self.configs['db']
        self.task = self.split_joint(self.configs['task'])

    def added_task(self, old_list):
        """
        添加任务列表
        :param old_list: 原有任务列表 list
        :return: 新的任务列表 list
        """
        r_list = list()
        for task in self.task:
            if task not in old_list:
                r_list.append(task)
        return r_list

    def merge(self, defaults, override):
        """
        合并配置文件
        :param defaults: 原配置文件 dict
        :param override: 新配置文件 dict
        :return: 合并后的配置文件 dict
        """
        r = {}
        for k, v in defaults.items():
            if k in override:
                if isinstance(v, dict):
                    r[k] = self.merge(v, override[k])
                else:
                    r[k] = override[k]
            else:
                r[k] = v
        return r

    def split_joint(self, d):
        """
        将task任务连接成字符串（模块名）
        :param d: task任务 dict/set
        :return: 连接后的任务列表 list
        """
        r_list = list()
        if isinstance(d, set):
            for i in d:
                r_list.append(re.sub(r'[^0-9a-zA-Z_]', '', i))
            return r_list
        elif isinstance(d, dict):
            for k, v in d.items():
                temp = self.split_joint(v)
                for i in temp:
                    t = re.sub(r'[^0-9a-zA-Z_]', '', k) + '_' + re.sub(r'[^0-9a-zA-Z_]', '', i)
                    r_list.append(t)
            return r_list
        else:
            return []
