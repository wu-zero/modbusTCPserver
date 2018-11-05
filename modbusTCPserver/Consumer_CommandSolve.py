from threading import Thread
import logging.handlers

CONSUMER_COMMANDSOLVE_LOG_FILENAME = '../log/command_solve_log/' + 'command_solve.log'

# logger的初始化工作
logger = logging.getLogger('command_solve_log')
logger.setLevel(logging.DEBUG)

# console_log
# 添加TimedRotatingFileHandler
# 定义一个1H换一次log文件的handler
# 保留20个旧log文件
data_file_handler = logging.handlers.TimedRotatingFileHandler(CONSUMER_COMMANDSOLVE_LOG_FILENAME, when='H', interval=1, backupCount=2)
data_file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
data_file_handler.setLevel(logging.INFO)
logger.addHandler(data_file_handler)


class Consumer_CommandSolve(Thread):
    """
    Consumer thread 消费线程，感觉来源于COOKBOOK
    """
    def __init__(self, t_name, queue, modbus,serial):
        Thread.__init__(self, name=t_name)
        self.data = queue
        self.serial = serial
        self.modbus = modbus

    def run(self):
        logger.info('CommandSolve begin')
        while True:
            #  更新系统时间
            self.modbus.updata_system_timestamp()

            # 处理命令
            try:
                args = self.data.get()
                self.solve_command(args,self.modbus,self.serial)
                logger.info('solve command ' + str(args))
            except:
                pass
            else:
                pass

    def solve_command(self,args, my_modbus, my_serial):
        if args[0] == 'data':
            my_modbus.updata_sensor_module(args[1])
        elif args[0] == 'reqtime':
            my_serial.write_time()
        elif args[0] == 'reset':
            pass
        elif args[0] == 'connect':
            pass
        elif args[0] == 'discnct':
            pass
        elif args[0] == 'devicelist':
            pass
