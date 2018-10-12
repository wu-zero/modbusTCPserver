import serial
from Convert import byte2_to_uint16
import sys


class MySerial:
    def __init__(self, port_address):
        self._ser = self._open_serial(port_address)

    def get_data_form_port(self):
        try:
            data = self._ser.readline()
            # result =[]
            # for i in range(10):
            #     a = byte2_to_uint16(data[i * 2:i * 2 + 2])
            #
            #     result.append(a)
            # print(result)
            return data
        except Exception as err:
            print("读取数据失败")
            print(err)


    @staticmethod
    def _open_serial(address):
        ser = serial.Serial()
        ser.baudrate = 115200
        ser.port = address
        ser.timeout = 1
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
    serial_address = '/dev/ttyUSB0'
    my_serial = MySerial(serial_address)
    for i in range(10):
        print(my_serial.get_data_form_port())


