import logging.handlers

import serial

import Setting
from utils.CyclicRedundancyCheck import crc16

Bytes_Num = 31
Bytes_End = b'\r\n'


# ==================================log相关开始=========================
MY_SERIAL_LOG_FILENAME = '../log/bottom_log/' + 'my_serial.log'

# logger的初始化工作
logger = logging.getLogger('my_serial')
logger.setLevel(logging.DEBUG)

# console_log
# 添加TimedRotatingFileHandler
# 定义一个1H换一次log文件的handler
# 保留2个旧log文件
handler = logging.handlers.TimedRotatingFileHandler(MY_SERIAL_LOG_FILENAME, when='H', interval=1, backupCount=2)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
handler.setLevel(logging.INFO)   
logger.addHandler(handler)
# ==================================log相关结束=======================


class MySerial:
    """自定义串口类，通过串口实现与ZigBee的数据、命令读写操作
    """
    
    def __init__(self):
        port_address = Setting.get_serial_address()
        self._ser = self._init_serial(port_address)

    #  ====================串口底层========================
    @staticmethod
    def _init_serial(address):
        """串口初始化
        
        Arguments:
            address {int} -- 串口地址
        
        Returns:
            serial -- 串口实列
        """

        ser = serial.Serial()
        ser.baudrate = 115200
        ser.port = address
        ser.timeout = 0.05  # 0.05
        try:
            ser.open()
        except Exception as err:
            print("端口打开失败，程序终止")
            print(err)

            # 退出程序
            import os
            import signal
            main_pid = os.getppid()
            print(main_pid)
            os.kill(os.getpid(), signal.SIGKILL)
        else:
            print('端口打开成功')
            return ser

    #  =====================应用===========================
    def get_data_form_port(self):
        """从ZigBee读取bytes,分析其含义(b'$'开头对应命令;b'\xaa'开头对应数据),
        返回命令处理线程能识别的命令
        
        Returns:
            list -- 命令处理线程能识别的命令
        """

        data_result = b''
        try:
            data_first = self._ser.read(1)
        except Exception:
            pass  # 串口读取错误。。。
        else:
            # 命令
            if data_first == b'':  # 没接到(正常)
                return None
            elif data_first == b'$':  # 接收到命令
                logger.info(data_first)
                try:
                    command = b''
                    while True:
                        data_command = self._ser.read(1)
                        if data_command == b'$':
                            break
                        else:
                            command = command + data_command
                except Exception:  # 命令字节接收错误
                    logger.error('command error '+str(command))
                    return None
                else:
                    #  判断命令类型
                    if command == b'reqtime':
                        return ['reqtime']
                    elif command == b'devicelist':
                        try:
                            data_num = self._ser.read(1)
                            num = ord(data_num)
                            result = []
                            for i in range(num):
                                result.append(ord(self._ser.read(1)))
                            return ['devicelist', result]
                        except Exception:
                            pass
                    else:  # 无效的命令类型
                        try:
                            data_result = command + self._ser.read_all()
                            logger.info('未知命令error ' + str(data_result))
                            return None
                        except Exception:
                            logger.info('未知命令error ' + str(command))
                            return None
            elif data_first == b'\xaa':  # 接收到数据
                logger.info(data_first)
                try:
                    data_result = data_first + self._ser.read(Bytes_Num-1)  # 31位
                    # 0xaa 1byte + 数据 26bytes + crc 2bytes + short_address 2bytes
                    if len(data_result) == Bytes_Num:  # 数据末尾加传感器模块短地址
                        data_data = data_result[:-4]
                        data_crc = data_result[-4:-2]
                        data_short_address = data_result[-2:]
                        if crc16(data_data, bytes_num=len(data_data)) == data_crc:
                            # print('getdata')
                            return ['data', data_data[1:]+data_short_address]
                        else:
                            logger.info('crc校验失败'+str(data_result))
                            return None  # crc校验失败
                    elif len(data_result) == Bytes_Num - 2:  # 数据末尾不加传感器模块短地址
                        data_data = data_result[:-2]
                        data_crc = data_result[-2:]
                        if crc16(data_data, bytes_num=len(data_data)) == data_crc:
                            return ['data', data_data[1:]]
                        else:
                            logger.info('crc校验失败' + str(data_result))
                            return None  # crc校验失败

                    else:
                        logger.info('数据长度错误'+str(data_result))
                except Exception:
                    logger.error('data error ' + str(data_result))
                    return None  # 数据字节接收错误
            else:
                try:
                    data_result = data_first + self._ser.read_all()
                    logger.info('未知数据error '+str(data_result))
                    return None
                except Exception:
                    logger.info('未知数据error '+str(data_first))
                    return None

    def write_time_to_zigbee(self):
        """通过串口向zigbee写系统时间(bytes)
        """

        time_bytes = Setting.get_time_bytes()
        self._ser.write(b'$settime$'+time_bytes)
        logger.info('$settime$ ' + str(time_bytes))

    def writ_command_to_zigbee(self, data_bytes):
        """通过串口向zigbee写命令(bytes)
        
        Arguments:
            data_bytes {bytes} -- 命令(bytes数据)
        """

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


if __name__ == '__main__':
    my_serial = MySerial()
    for i in range(10):
        data = my_serial.get_data_form_port()
        print(data)
        print(len(data))
