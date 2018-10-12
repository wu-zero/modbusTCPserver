from MySerial import MySerial
from MyModbus import MyModbus
import Convert


if __name__ == '__main__':
    serial_address = '/dev/ttyUSB0'



    my_serial = MySerial(serial_address)
    my_modbus = MyModbus()
    my_modbus.set_system_parameter()


    while True:
        data = my_serial.get_data_form_port()
        my_modbus.updata(data)




