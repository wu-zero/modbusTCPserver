import logging.handlers
import time
from threading import Thread

CONSUMER_COMMANDSOLVE_LOG_FILENAME = '../log/command_solve_log/' + 'command_solve.log'

# logger的初始化工作
logger = logging.getLogger('command_solve_log')
logger.setLevel(logging.DEBUG)

# console_log
# 添加TimedRotatingFileHandler
# 定义一个1H换一次log文件的handler
# 保留5个旧log文件
handler = logging.handlers.TimedRotatingFileHandler(CONSUMER_COMMANDSOLVE_LOG_FILENAME, when='H', interval=1, backupCount=5)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
handler.setLevel(logging.INFO)
logger.addHandler(handler)


class Consumer_CommandSolve(Thread):
    """
    Consumer thread 消费线程
    """
    def __init__(self, t_name, queue, modbus, serial, monitor):
        Thread.__init__(self, name=t_name)
        self.queue = queue
        self.serial = serial
        self.modbus = modbus
        self.monitor = monitor

    #  线程运行
    def run(self):
        try:
            print('命令处理线程开始执行', time.time())
            logger.info('CommandSolve begin')
            while True:
                try:
                    # 处理命令
                    if not self.queue.empty():
                        args = self.queue.get()
                        self._solve_command(args, self.modbus, self.serial, self.monitor)
                        logger.info('solve command ' + str(args))
                except Exception as err:
                    print(err)
                    pass
                else:
                    pass
        except Exception:
            pass

    #  命令处理
    @staticmethod
    def _solve_command(args, modbus, serial, monitor):
        if args[0] == 'data':
            if monitor.monitor_module_timestamp(args[1]):
                modbus.update_sensor_module(args[1])
        elif args[0] == 'reqtime':
            serial.write_time_to_zigbee()
        elif args[0] == 'devicelist' and len(args) == 2:
            print(args)
        elif args[0] == 'devicelist' and len(args) == 1:
            serial.writ_command_to_zigbee(b'$devicelist$')
        elif args[0] == 'reset':
            value = b'$reset$' + args[1].to_bytes(1, byteorder='little')
            serial.writ_command_to_zigbee(value)
        elif args[0] == 'hbfreq':
            value = b'$hbfreq$' + args[1].to_bytes(1, byteorder='little')
            serial.writ_command_to_zigbee(value)
        elif args[0] == 'set extern address':
            value = b'$extaddr$' + args[1].to_bytes(8, byteorder='little')
            serial.writ_command_to_zigbee(value)
        elif args[0] == 'connect':
            pass
        elif args[0] == 'discnct':
            pass
        elif args[0] == 'devicelist':
            pass
