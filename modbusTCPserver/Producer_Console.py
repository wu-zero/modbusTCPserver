from threading import Thread,Event
import sys
from queue import Queue
from prompt_toolkit import prompt
import logging.handlers
import time

PRODUCER_CONSOLE_LOG_FILENAME = '../log/console_log/' + 'console.log'

# logger的初始化工作
logger = logging.getLogger('console_log')
logger.setLevel(logging.DEBUG)

# console_log
# 添加TimedRotatingFileHandler
# 定义一个1H换一次log文件的handler
# 保留2个旧log文件
data_file_handler = logging.handlers.TimedRotatingFileHandler(PRODUCER_CONSOLE_LOG_FILENAME, when='H', interval=1, backupCount=2)
data_file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
data_file_handler.setLevel(logging.INFO)
logger.addHandler(data_file_handler)


class Producer_Console(Thread):
    """
    Producer thread 制作线程
    """
    def __init__(self, t_name, queue):  # 传入线程名、实例化队列
        Thread.__init__(self, name=t_name)  # t_name即是threadName
        self.data = queue
        self.exit = Event()

    def run(self):
        try:
            print('控制台 线程开始执行', time.time())
            logger.info('Console begin')
            while not self.exit.is_set():
                try:
                    input_data = prompt('>')  # sys.stdin.readline()
                except Exception:
                    print('Console_error')
                    pass
                else:
                    if input_data == 'quit':
                        self.stop()
                    else:
                        args = self.input_data_solve(input_data)
                        if args is not None:
                            self.data.put(args)  # 写入队列编号
                            logger.info('get command ' + str(args))
            print('Console exit')
            logger.info('Console exit')
        except Exception:
            pass

    def input_data_solve(self, data):
            data_list = list(filter(None, data.split('$')))
            if len(data_list) == 1 and data_list[0] == 'reqtime':
                print('get command: reqtime')
                return ['reqtime']
            elif len(data_list) == 1 and data_list[0] == 'devicelist':
                print('get command: devicelist')
                return ['devicelist']
            elif len(data_list) == 2 and data_list[0] == 'reset':
                try:
                    arg = int(data_list[1])
                except Exception as err:
                    sys.stdout.write('you should input: $reset$ [Uint8]\n')
                    return None
                else:
                    if 0 <= arg <= 2 ** 8 - 1:
                        print('get command: reset ',arg)
                        return ['reset', arg]
                    else:
                        sys.stdout.write('you should input: $reset$ [Uint8](0~255)\n')
                        return None
            elif len(data_list) == 2 and data_list[0] == 'hbfreq':
                try:
                    arg = int(data_list[1])
                except Exception as err:
                    sys.stdout.write('you should input: $hbfreq$ [Uint8]\n')
                    return None
                else:
                    if 0 <= arg <= 2 ** 8 - 1:
                        print('get command: hbfreq ', arg)
                        return ['hbfreq', arg]
                    else:
                        sys.stdout.write('you should input: $hbfreq$ [Uint8](0~255)\n')
                        return None
            elif len(data_list) == 2 and data_list[0] == 'reset':
                try:
                    arg = int(data_list[1])
                except Exception as err:
                    sys.stdout.write('you should input: $reset$ [Uint8]\n')
                    return None
                else:
                    if 0 <= arg <= 2 ** 8 - 1:
                        print('get command: reset ', arg)
                        return ['reset', arg]
                    else:
                        sys.stdout.write('you should input: $reset$ [Uint8](0~255)\n')
                        return None
            else:
                print("unknown command")
                return None

    def stop(self):
        self.exit.set()


if __name__ == '__main__':
    queue = Queue()  # 队列实例化
    producer2 = Producer_Console('console',queue)
    producer2.start()  # 开始制造
    """
    join（）的作用是，在子线程完成运行之前，这个子线程的父线程将一直被阻塞。
　　join()方法的位置是在for循环外的，也就是说必须等待for循环里的两个进程都结束后，才去执行主进程。
    """
    producer2.join()

    while True:
        try:
            arg = queue.get()
            print(arg)

        except:
            sys.exit()
        else:
            pass