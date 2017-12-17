import threadpool
import time
import importlib
import datetime

from frame import config
from frame import database

"""
使用线程池做任务分发调度。
"""


class Schedule(object):
    TASK = 'task'
    THREADPOOL_COUNT = 4

    def __init__(self):
        """
        创建线程池，循环读取配置，提取任务，根据时间间隔添加任务，执行任务
        """
        print("Creating thread pool with %s worker threads." % self.THREADPOOL_COUNT)
        self.thread_pool = threadpool.ThreadPool(self.THREADPOOL_COUNT)

        self.l_task = list()
        self.time_task_list = list()

        con = config.Config()
        print(con.task)
        self.db = database.DataBase(con.db)
        while True:
            con = config.Config()
            self.l_add_task = con.added_task(self.l_task)
            self.l_task = con.task

            for task in self.l_add_task:
                self.add_task(task)

            current = datetime.datetime.now().timestamp()
            for d in self.time_task_list[:]:
                if d['time'] <= current:
                    if d['module_name'] in self.l_task:
                        self.add_task(d['module_name'])
                    self.time_task_list.remove(d)

            try:
                time.sleep(0.1)
                # print("(active worker threads: %i)" % (threadpool.threading.activeCount() - 1,))
                self.thread_pool.poll()
            except KeyboardInterrupt:
                print("**** Interrupted!")
                break
            except threadpool.NoResultsPending:
                pass
                # print("**** No pending results.")

        if self.thread_pool.dismissedWorkers:
            print("Joining all dismissed worker threads...")
            self.thread_pool.joinAllDismissedWorkers()

    def add_task(self, task):
        """
        将任务添加到线程池队列中
        :param task: 任务模块名 str
        :return: 无
        """
        data = [((task,), {'db': self.db})]
        requests = threadpool.makeRequests(self.thread_fun, data, self.callback, self.handle_exception)
        for req in requests:
            self.thread_pool.putRequest(req)
            print("callback Work request #%s added." % (req.requestID,))

    def callback(self, request, result):
        """
        线程池的必备函数，对任务的返回值进行处理
        :param request: 任务编号
        :param result: 返回值
        :return: 无
        """
        print("**** Result from request #%s: %r" % (request.requestID, result))
        if result['loop'] and result['interval'] >= 0:
            result['time'] = datetime.datetime.now().timestamp() + result['interval']
            self.time_task_list.append(result)

    def thread_fun(self, *args, **kwargs):
        """
        线程池的必备函数，运行函数
        :param args: args[0]是task 模块名
        :param kwargs: kwargs['db'] 数据库句柄
        :return: 任务的返回值
        """
        try:
            task_module = importlib.import_module(self.TASK + '.' + args[0])
        except ModuleNotFoundError:
            raise
        except Exception:
            raise
        result = task_module.Task(args[0], kwargs['db'])
        # result 应该 args[0]也就是task任务文件名。interval间隔时间 dict形式
        return result.get_result()

    def handle_exception(self, request, exc_info):
        """
        线程池的可选函数，异常处理
        :param request: 任务编号
        :param exc_info: 异常信息
        :return: 无
        """
        if not isinstance(exc_info, tuple):
            # Something is seriously wrong...
            print(self, request)
            print(exc_info)
            raise SystemExit
        print("**** Exception occured in request #%s: %s" % (request.requestID, exc_info))


if __name__ == '__main__':
    # a = Schedule(['okcoincn_rest_btc_ticker', 'okcoincn_rest_ltc_ticker', '3', '4', '5'], 'db')
    pass
