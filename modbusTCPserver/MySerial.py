import sys
import logging.handlers
import serial

import Setting
from CyclicRedundancyCheck import crc16


Bytes_Num = 32
Bytes_End = b'\r\n'



MY_SERIAL_LOG_FILENAME = '../log/bottom_log/' + 'my_serial.log'

# logger的初始化工作
logger = logging.getLogger('my_serial')
logger.setLevel(logging.DEBUG)

# console_log
# 添加TimedRotatingFileHandler
# 定义一个1H换一次log文件的handler
# 保留20个旧log文件
file_handler = logging.handlers.TimedRotatingFileHandler(MY_SERIAL_LOG_FILENAME, when='H', interval=1, backupCount=2)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
file_handler.setLevel(logging.INFO)   # ===============
logger.addHandler(file_handler)






class MySerialException(Exception):
    def __init__(self, err=' 串口错误'):
        Exception.__init__(self, err)


class MySerial:
    def __init__(self):
        port_address = Setting.get_serial_address()
        self._ser = self._init_serial(port_address)

    def get_data_form_port(self):
        data_result = b''
        try:
            data = self._ser.read(1)

        except:
            pass  # 没收到(正常)
        else:
            # 命令
            if data == b'':  # 没接到(正常)
                return None
            elif data == b'$':  # 命令
                try:
                    command = b''
                    while True:
                        data = self._ser.read(1)
                        if data == b'$':
                            break
                        else:
                            command = command + data
                except Exception:  # 命令字节接收错误
                    logger.error('command error '+str(command))
                    return None
                else:
                    #  判断命令类型
                    if command == b'reqtime':
                        return ['reqtime']
                    elif command == b'devicelist':
                        try:
                            data = self._ser.read(1)
                            num = ord(data)
                            result = []
                            for i in range(num):
                                result.append(ord(self._ser.read(1)))
                            return ['devicelist',result]
                        except Exception:
                            pass
                    else:  # 无效的命令类型
                        try:
                            data_result = command + self._ser.read_all()
                            logger.info('未知命令error ' + str(data_result))
                            return None
                        except:
                            logger.info('未知命令error ' + str(command))
                            return None
            elif ord(data) == 0xaa:  # 数据
                try:
                    data_result = data + self._ser.read(32) # 33位
                    if crc16(data_result[:-2],bytes_num=31) == data_result[-2:]:
                        #print('getdata')
                        return ['data',data_result[1:-2]]
                    else:
                        return None  # crc校验失败
                except Exception:
                    logger.error('data error ' + str(data_result))
                    return None  # 数据字节接收错误
            else:
                try:
                    data_result = data + self._ser.read_all()
                    logger.info('未知数据error '+str(data_result))
                    return None
                except:
                    logger.info('未知数据error '+str(data))
                    return None

    def write_time(self):
        time_bytes = Setting.get_time_bytes()
        self._ser.write(b'$settime$'+time_bytes)
        logger.info('$settime$ ' + str(time_bytes))

    def writ_command_to_zigbee(self,data_bytes):
        logger.info(str(data_bytes))
        self._ser.write(data_bytes)
        # data = self._ser.readline()
        # data_result = data_result + data
        # print(data_result.decode())
        # if data_result[0:len(b'$data$')] == b'$data$':
        #     command_type = 'data'
        #     bytes_num = 38 # 6+2+7*4+2
        # elif data_result[0:len(b'$reqtime$')] == b'$reqtime$':
        #     command_type = 'reqtime'
        #     bytes_num = 11  # 9+2
        # elif data_result[0:len(b'$connect$')] == b'$connect$':
        #     command_type = 'connect'
        #     bytes_num = 12  # 9+1+2
        # elif data_result[0:len(b'$discnct$')] == b'$discnct$':
        #     command_type = 'discnct'
        #     bytes_num = 12  # 9+1+2
        # elif data_result[0:len(b'$devicelist$')] == b'$devicelist$':
        #     command_type = 'devicelist'
        #     num = ord(data_result[len(b'$devicelist$'):len(b'$devicelist$')+1])
        #     bytes_num = 15+num   #12 + 1 + num + 2
        # else:
        #     command_type = 'data'
        #     bytes_num = 38  # 6+2+7*4+2
        #
        # data_result = self.get_right_data(data_result,bytes_num)
        #
        # return data_result

    @staticmethod
    def _init_serial(address):
        ser = serial.Serial()
        ser.baudrate = 115200
        ser.port = address
        ser.timeout = 0.05 #0.05
        try:
            ser.open()
        except Exception as err:
            print("端口打开失败，程序终止")
            print(err)
            sys.exit()
        else:
            print('端口打开成功')
            return ser


if __name__ == '__main__':
    my_serial = MySerial()
    for i in range(10):
        data = my_serial.get_data_form_port()
        print(data)
        print(len(data))

