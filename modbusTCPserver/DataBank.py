import time
import Convert

SYS_PARAMETER_ADDRESS = 4000-1

SENSOR_MODULES_ADDRESS = {1: 4021 - 1, 2: 4051 - 1, 3: 4081 - 1, 4: 4111 - 1, 5: 4141 - 1}
SENSOR_MODULES_ID = list(SENSOR_MODULES_ADDRESS.keys())


class Databank(object):
    def __init__(self):
        self.sys_parameter = SysParameter(SYS_PARAMETER_ADDRESS)
        self._sensor_module = {}
        for sensors_module_id, sensors_module_address in SENSOR_MODULES_ADDRESS.items():
            self._add_sensor_module(sensors_module_id, sensors_module_address)

    def get_sys_parameter_address_and_values(self):
        return self.sys_parameter.get_address_and_values()

    def get_sys_parameter_timestamp_address_and_values(self):
        return self.sys_parameter.get_timestamp_address_and_values()

    def get_sensor_module_address_and_values(self, sensor_module_id):
        sensor_module = self._sensor_module[sensor_module_id]
        return sensor_module.get_address_and_values()

    def get_sensor_module_address_values_and_realvalues_when_update(self, data_bytes):

        values = []
        Convert.convert_to_uint16_data(values, 'bytes', data_bytes[0:2])
        sensor_module_id = values[0]
        data_bytes = data_bytes[2:-2]
        sensor_module = self._sensor_module[sensor_module_id]
        return sensor_module.get_address_values_and_realvalues_when_update(data_bytes)



    # 打开的传感器模块id list
    def sensor_modules_on_list(self):
        result = []
        for sensor_module_id,sensor_module in self._sensor_module.items():
            if sensor_module.is_on():
                result.append(sensor_module_id)
        return result

    # 传感器模块id
    def sensor_module_list(self):
        return list(self._sensor_module.keys())

    # 关传感器模块
    def off_sensor_module(self, module_id):
        if self._if_include_module(module_id):
            self._sensor_module[module_id].off()

    # 开传感器模块
    def on_sensor_module(self, module_id):
        if self._if_include_module(module_id):
            self._sensor_module[module_id].on()

    def _if_include_module(self, module_id):
        return module_id in self._sensor_module.keys()

    # 初始化时添加传感器模块
    def _add_sensor_module(self, sensors_module_id, address):
        self._sensor_module[sensors_module_id] = SensorsModule(sensors_module_id, address)


class SysParameter:
    def __init__(self,address_begin):
        self.address = address_begin
        self.parts = [
            'version_num',
            'unit_num',
            'sensor_num',
            'time_stamp']
        self.config ={
            'version_num': [0, 'uint16', 1],
            'unit_num':    [1, 'uint16', 0],
            'sensor_num':  [2, 'uint16', 5],
            'time_stamp':  [3, 'uint32', int(time.time())],
            'reserve':     [5, 'unknow',0]
            }

    # 初始化时，获取起始地址和要写入的值
    def get_address_and_values(self):
        address_begin = self.address
        values = []
        for part in self.parts:
            Convert.convert_to_uint16_data(values, self.config[part][1], self.config[part][2])
        return address_begin, values

    # 更新时间戳时，获取时间戳起始地址要写入的值
    def get_timestamp_address_and_values(self):
        address_begin = self.address + self.config['time_stamp'][0]
        values = []
        Convert.convert_to_uint16_data(values, self.config['time_stamp'][1], int(time.time()))
        return address_begin, values


class SensorsModule:
    def __init__(self, module_id,address):
        self.address = address
        self.module_id = module_id
        self._is_on = False
        self.parts = [
            'module_id',
            'install_num',
            'temperature',
            'humidity',
            'o3',
            'voc',
            'co2',
            'pm2.5',
            'time_stamp',
            'reserve']
        self.config = {
            'module_id': [0, 'uint16', module_id],
            'install_num': [1, 'char*10', 'YTHA-'+str(module_id)],
            'temperature': [6, 'float', 0.0],
            'humidity': [8, 'float', 0.0],
            'o3': [10, 'float', 0.0],
            'voc': [12, 'float', 0.0],
            'co2': [14, 'float', 0.0],
            'pm2.5': [16, 'float', 0.0],
            'time_stamp': [18, 'uint32', int(time.time())],
            'reserve': [20, 'unknow', 0]
            }

    # 初始化时，获取起始地址和要写入的值
    def get_address_and_values(self):
        address_begin = self.address
        values = []
        for part in self.parts:
            Convert.convert_to_uint16_data(values, self.config[part][1], self.config[part][2])
        return address_begin, values

    # 更新数据时，获取起始地址和要写入的值和真实值（用于log）
    def get_address_values_and_realvalues_when_update(self, data_bytes):
        address_begin = self.address + self.config['temperature'][0]
        values = []
        Convert.convert_to_uint16_data(values, 'bytes', data_bytes)
        realvalues = []
        # 添加数据
        for sensor_module_part in self.parts[2:]:
            Convert.convert_to_real_data(realvalues, self.config[sensor_module_part][1],
                                         data_bytes[(self.config[sensor_module_part][0] - 6) * 2:])
        return address_begin,values,realvalues


    def off(self):
        self._is_on = False
    def on(self):
        self._is_on = True
    def is_on(self):
        return self._is_on


if __name__ == '__main__':
    databank = Databank()
    databank.on_sensor_module(1)
    databank.on_sensor_module(5)

    print(databank.sensor_modules_on_list())
    print(databank.get_sys_parameter_timestamp_address_and_values())
    print(databank.get_sys_parameter_address_and_values())
    print(databank.get_sensor_module_address_and_values(2))
    print(databank.get_sensor_module_address_and_values(3))
    print(databank.sensor_module_list())
    print(databank.sensor_modules_on_list())
    a = b'\4\0cdefglskjdfdsddddewwwwwwwwww\r\n'
    print(databank.get_sensor_module_address_values_and_realvalues_when_update(data_bytes=a))