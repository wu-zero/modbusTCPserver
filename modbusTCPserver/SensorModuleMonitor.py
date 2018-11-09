import Setting
import time
import logging.handlers

MONITOR1_LOG_FILENAME = '../log/monitor_log/' + 'monitor.log'




# logger的初始化工作
logger = logging.getLogger('monitor1_log')
logger.setLevel(logging.DEBUG)


# 数据log
# 添加TimedRotatingFileHandler
# 定义一个1H换一次log文件的handler
# 保留5个旧log文件
file_handler = logging.handlers.TimedRotatingFileHandler(MONITOR1_LOG_FILENAME, when='D', interval=1, backupCount=5)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)





class SensorModuleMonitor:

    def __init__(self):

        self.timestamp_dict = {}
        time_now = int(time.time())
        for module_id in Setting.Sensor_Module_Id_List:
            self.timestamp_dict[module_id] = time_now

        self.off_line_bool_dict_old = {}
        for module_id in Setting.Sensor_Module_Id_List:
            self.off_line_bool_dict_old[module_id] = 1

        logger.info('设备重启。。。。。')


    def updata_timestamp(self,data_bytes):
        module_id, time_stamp = Setting.get_module_id_and_timestamp_from_bytes(data_bytes)
        if module_id in Setting.Sensor_Module_Id_List:
            self.timestamp_dict[module_id] = time_stamp

    def monitor(self):
        time_now = int(time.time())
        off_line_bool_dict = {}
        for module_id in Setting.Sensor_Module_Id_List:
            if time_now - self.timestamp_dict[module_id] > 3:
                off_line_bool_dict[module_id] = 1
            else:
                off_line_bool_dict[module_id] = 0

            if self.off_line_bool_dict_old[module_id] == 1 and off_line_bool_dict[module_id] == 0:
                logger.info('模块'+str(module_id) + ' on line')
            if self.off_line_bool_dict_old[module_id] == 0 and off_line_bool_dict[module_id] == 1:
                logger.info('模块' + str(module_id) + ' off line')

        self.off_line_bool_dict_old = off_line_bool_dict

