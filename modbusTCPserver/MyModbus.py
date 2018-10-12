import sys
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
from modbus_tk.exceptions import(
    ModbusError, ModbusFunctionNotSupportedError, DuplicatedKeyError, MissingKeyError, InvalidModbusBlockError,
    InvalidArgumentError, OverlapModbusBlockError, OutOfModbusBlockError, ModbusInvalidResponseError,
    ModbusInvalidRequestError
)
import time
import Convert
modules_address = \
    {'system_parameter': 4000,
        'sensor1': 4021,
        'sensor2': 4051,
        'sensor3': 4081,
        'sensor4': 4111,
        'sensor5': 4141}


system_parameter = [
    'version_num',
    'unit_num',
    'sensor_num',
    'time_stamp']
sensor = [
    'module_num',
    'install_num',
    'temperature',
    'humidity',
    'o3',
    'voc',
    'co2',
    'pm2.5',
    'time_stamp',
    'reserve']
#     name  address+  type   初始值
system_parameter_config = {
    'version_num': [0, 'uint16', 1],
    'unit_num':    [1, 'uint16', 0],
    'sensor_num':  [2, 'uint16', 5],
    'time_stamp':  [3, 'uint32', 65536],#int(time.time())]
    'reserve':     [5, 'unknow',0]
}

sensor_config = {
    'module_num': [0, 'uint16', 1],
    'install_num': [1, 'char*10', 'YTHA-7'],
    'temperature': [6, 'float', 0.0],
    'humidity': [8, 'float', 0.0],
    'o3': [10, 'float', 1.1],
    'voc': [12, 'float', 0.0],
    'co2': [14, 'float', 0.0],
    'pm2.5': [16, 'float', 0.0],
    'time_stamp': [18, 'uint32', int(time.time())],
    'reserve': [0, 'unknow', 0]
}


class MyModbus:
    def __init__(self):    
        # 初始化
        self._slave_id = 1
        self._block_name = ['b1', 'b2', 'b3', 'b4']

        self.logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")
        self.server = modbus_tcp.TcpServer(address='0.0.0.0', port=502)
        self.logger.info("running...")
        # 服务启动
        self.server.start()
        # 建立从机
        self.slave = self.server.add_slave(self._slave_id)
        # 建立块
        #slave.add_block('b1', cst.DISCRETE_INPUTS, 0, 100)
        #slave.add_block('b2', cst.COILS, 0, 100)
        self.slave.add_block(self._block_name[2], cst.ANALOG_INPUTS, 3999, 4169)
        #slave.add_block('b4', cst.HOLDING_REGISTERS, 0, 100)

    def set_system_parameter(self):
        address_begin = modules_address['system_parameter'] - 1
        values = []
        for i in system_parameter:
            print(system_parameter_config[i])
            Convert.add_data(values,system_parameter_config[i][1],system_parameter_config[i][2])
        self.slave.set_values(self._block_name[2],address_begin,values)

    def set_sensor(self):
        address_begin = modules_address['sensor1'] - 1
        values = []
        for i in sensor:
            print(sensor_config[i])
            Convert.add_data(values, sensor_config[i][1], sensor_config[i][2])
        self.slave.set_values(self._block_name[2], address_begin, values)


    def updata(self,data):
        data_convert = []
        Convert.add_data(data_convert, 'bytes', data)
        print(data_convert)
        sensor_id = data_convert[0]
        values = data_convert[1:]
        if sensor_id == 0:
            address_begin = modules_address['sensor1']

            print(values)
            print(data)
            self.slave.set_values(self._block_name[2], address_begin, values)



    #
    # def set_input_registers_value(begin_address, values=None):
    #     name = block_name[2]
    #     if values is None:
    #         print('值错误')
    #         return
    #     else:
    #         values = list(values)
    #
    #     try:
    #         slave.set_values(name, begin_address, values)
    #     except Exception as err:
    #         sys.stdout.write(str(err) + '\r\n')
    #     else:
    #         values = slave.get_values(name, begin_address, len(values))
    #         sys.stdout.write('done: values written: %s\r\n' % str(values))
    #





if __name__ == "__main__":
   my_modbus = MyModbus()
   a = [1]
   my_modbus.set_system_parameter()
   my_modbus.set_sensor()
   my_modbus.updata(b'\0\0\0aa\0')