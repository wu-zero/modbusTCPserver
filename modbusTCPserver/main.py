from MySerial import MySerial
from MyModbus import MyModbus
import Convert


if __name__ == '__main__':
    serial_address = '/dev/ttyUSB1'



    my_serial = MySerial(serial_address)
    my_modbus = MyModbus()
    my_modbus.set_system_parameter()
    my_modbus.set_sensors()

    while True:
        my_modbus.updata_system_timestamp()
        try:
            data = my_serial.get_data_form_port()
        except Exception as err:
            print(err)
        else:
            my_modbus.updata2(data)




