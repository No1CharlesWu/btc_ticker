class TaskBase(object):
    """
    任务类父类
    """

    # TODO:完善任务类
    def __init__(self, module_name, db):
        """
        :param module_name: 子类名称
        :param db: 数据库句柄
        """
        self.do_before(module_name, db)
        self.do()
        self.do_after()

    def do_before(self, module_name, db):
        """
        具体初始化
        :param module_name: 子类名称
        :param db: 数据库句柄
        :return: 无
        """
        # print('TaskBase init', db)
        self.db = db
        self.module_name = module_name
        self.set_interval()

    def do(self):
        """
        具体任务，子类继承
        :return: 无
        """
        pass

    def do_after(self):
        """
        善后处理
        :return: 无
        """
        pass

    def set_interval(self, interval=-1):
        """
        设置下次添加此任务的间隔时间，若不设置，则self.loop = False self.interval = -1 为不再添加此项任务
        :param interval: 间隔时间
        :return: 无
        """
        if interval >= 0:
            self.loop = True
        else:
            self.loop = False
        self.interval = interval

    def get_result(self):
        """
        返回值
        :return: 模块名，是否循环，间隔时间 dict
        """
        r = dict()
        r['module_name'] = self.module_name
        r['loop'] = self.loop
        r['interval'] = self.interval
        return r
