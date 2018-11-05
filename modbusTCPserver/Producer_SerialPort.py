from threading import Thread
import logging.handlers

PRODUCER_SERIALPORT_LOG_FILENAME = '../log/serial_port_log/' + 'serial_port.log'

# logger的初始化工作
logger = logging.getLogger('serial_port_log')
logger.setLevel(logging.DEBUG)

# console_log
# 添加TimedRotatingFileHandler
# 定义一个1H换一次log文件的handler
# 保留20个旧log文件
data_file_handler = logging.handlers.TimedRotatingFileHandler(PRODUCER_SERIALPORT_LOG_FILENAME, when='H', interval=1, backupCount=2)
data_file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
data_file_handler.setLevel(logging.INFO)
logger.addHandler(data_file_handler)


class Producer_Serial(Thread):
    """
    Producer thread 制作线程
    """
    def __init__(self, t_name, queue, serial):  # 传入线程名、实例化队列
        Thread.__init__(self, name=t_name)  # t_name即是threadName
        self.data = queue
        self.serial = serial


    """
    run方法 和start方法:
    它们都是从Thread继承而来的，run()方法将在线程开启后执行，
    可以把相关的逻辑写到run方法中（通常把run方法称为活动[Activity]）；
    start()方法用于启动线程。
    """
    def run(self):
        logger.info('serial_port begin')
        while True:
            args = self.serial.get_data_form_port()  # serial 读命令
            if args is not None:
                self.data.put(args)  # 写入队列编号
                logger.info('get command ' + str(args))
