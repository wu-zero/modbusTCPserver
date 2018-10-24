from MySerial import MySerial
from MyModbus import MyModbus
from MyLog import logger
import Setting

if __name__ == '__main__':
    my_serial = MySerial()
    my_modbus = MyModbus()


    while True:
        my_modbus.updata_system_timestamp()
        try:
            data = my_serial.get_data_form_port()
        except Exception as err:
            print(err)
        else:
            logger.info(Setting.get_real_data(data))
            my_modbus.updata2(data)




