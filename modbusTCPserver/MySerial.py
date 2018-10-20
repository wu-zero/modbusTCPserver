import serial
from Convert import byte2_to_uint16
import sys


Bytes_Num = 32
Bytes_End = b'\r\n'

class MySerialException(Exception):
    def __init__(self, err=' 串口错误'):
        Exception.__init__(self, err)



class MySerial:
    def __init__(self, port_address):
        self._ser = self._open_serial(port_address)

    def get_data_form_port(self):
        data_result = b''
        while True:
            data = self._ser.readline()
            data_result = data_result + data
            # print(len(data_result))
            if data_result[-2:] == Bytes_End:
                if len(data_result) == Bytes_Num:
                    return data_result[:-2]
                elif len(data_result) > Bytes_Num:
                    raise MySerialException('接收数据错误')
                else:
                    pass
            else:
                if len(data_result) >= Bytes_Num:
                    raise MySerialException('接收数据错误')
                else:
                    pass



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
    serial_address = '/dev/ttyUSB1'
    my_serial = MySerial(serial_address)
    for i in range(10):
        data = my_serial.get_data_form_port()
        print(data)
        print(len(data))

