import Setting
import time
import logging.handlers

MONITOR1_LOG_FILENAME = '../log/monitor_log/' + 'online_monitor.log'
MONITOR2_LOG_FILENAME = '../log/monitor_log/' + 'loss_data_monitor.log'




# logger的初始化工作
logger1 = logging.getLogger('monitor1_log')
logger1.setLevel(logging.DEBUG)

logger2 = logging.getLogger('monitor2_log')
logger2.setLevel(logging.DEBUG)




# 数据log
# 添加TimedRotatingFileHandler
# 定义一个1H换一次log文件的handler
# 保留5个旧log文件
handler = logging.handlers.TimedRotatingFileHandler(MONITOR1_LOG_FILENAME, when='D', interval=1, backupCount=5)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
handler.setLevel(logging.INFO)
logger1.addHandler(handler)

handler2 = logging.handlers.TimedRotatingFileHandler(MONITOR2_LOG_FILENAME, when='D', interval=1, backupCount=5)
handler2.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
handler2.setLevel(logging.INFO)
logger2.addHandler(handler2)



class SensorModuleMonitor:

    def __init__(self):

        self.timestamp_dict = {}
        self.timestamp_dict_old = {}
        time_now = int(time.time())
        for module_id in Setting.Sensor_Module_Id_List:
            self.timestamp_dict[module_id] = time_now
            self.timestamp_dict_old[module_id] = time_now

        self.off_line_bool_dict_old = {}
        for module_id in Setting.Sensor_Module_Id_List:
            self.off_line_bool_dict_old[module_id] = 1

        logger1.info('设备重启。。。。。')
        logger2.info('设备重启。。。。。')


    def updata_timestamp(self,data_bytes):
        return True
        module_id, time_stamp = Setting.get_module_id_and_timestamp_from_bytes(data_bytes)
        if module_id in Setting.Sensor_Module_Id_List:
            time_difference = time_stamp - self.timestamp_dict[module_id]
            if time_difference >= 0:
                self.timestamp_dict_old = self.timestamp_dict
                self.timestamp_dict[module_id] = time_stamp

                if time_difference > 5 and self.off_line_bool_dict_old[module_id] != 1:
                    logger2.info('模块'+str(module_id)+'不合理时间间隔：'+str(time_difference))

                return True
            else:
                return False

    def monitor(self):
        time_now = int(time.time())
        off_line_bool_dict = {}
        for module_id in Setting.Sensor_Module_Id_List:
            if time_now - self.timestamp_dict[module_id] > 30:
                off_line_bool_dict[module_id] = 1
            else:
                off_line_bool_dict[module_id] = 0

            if self.off_line_bool_dict_old[module_id] == 1 and off_line_bool_dict[module_id] == 0:
                logger1.info('模块' + str(module_id) + ' on line')
            if self.off_line_bool_dict_old[module_id] == 0 and off_line_bool_dict[module_id] == 1:
                logger1.info('模块' + str(module_id) + ' off line')

        self.off_line_bool_dict_old = off_line_bool_dict

