import time
import logging
import logging.handlers

import Setting

data_log_filename = '../log/data_log/'+'data.log'
error_log_filename = '../log/error_log/'+'error.log'


# logger的初始化工作
logger = logging.getLogger('my_log')
logger.setLevel(logging.DEBUG)


# 数据log
# 添加TimedRotatingFileHandler
# 定义一个1H换一次log文件的handler
# 保留20个旧log文件
data_file_handler = logging.handlers.TimedRotatingFileHandler(data_log_filename, when='H', interval=1, backupCount=2)
# 设置后缀名称，跟strftime的格式一样
#data_file_handler.suffix = "%Y-%m-%d_%H-%M-%S.log"#"%Y-%m-%d_%H-%M-%S.log"

data_file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
data_file_handler.setLevel(logging.INFO)


# 运行log
# 添加TimedRotatingFileHandler
# 定义一个1H换一次log文件的handler
# 保留5个旧log文件
error_file_hander = logging.handlers.TimedRotatingFileHandler(error_log_filename, when='H', interval=1, backupCount=5)
# 设置后缀名称，跟strftime的格式一样
#error_file_hander.suffix = "%Y-%m-%d_%H.log"

error_file_hander.setLevel(logging.ERROR)
error_file_hander.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

#控制台
console = logging.StreamHandler()

console.setLevel(logging.ERROR)
console.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))



# 添加hander
logger.addHandler(data_file_handler)
logger.addHandler(error_file_hander)
if Setting.CONSOLE_LOG_FLAG:
    logger.addHandler(console)


if __name__ == '__main__':
    while True:
        time.sleep(0.1)
        logger.info("file test")
        logger.error("error22222")
