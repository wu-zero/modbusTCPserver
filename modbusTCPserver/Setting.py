import time
from copy import deepcopy
import Convert

Modules_Address = {
    'system_parameter': 4000-1,
    'sensors': 4021-1}
# sensors_id  sensors_name sensors_address
System_Parameter = [
    'version_num',
    'unit_num',
    'sensor_num',
    'time_stamp']
System_Parameter_Config = {
    'version_num': [0, 'uint16', 1],
    'unit_num':    [1, 'uint16', 0],
    'sensor_num':  [2, 'uint16', 5],
    'time_stamp':  [3, 'uint32', int(time.time())],
    'reserve':     [5, 'unknow',0]
}
sensor = [
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
#     name  address+  type   初始值
Sensor_Config = {
    'module_id': [0, 'uint16', 1],
    'install_num': [1, 'char*10', 'YTHA-7'],
    'temperature': [6, 'float', 0.0],
    'humidity': [8, 'float', 0.0],
    'o3': [10, 'float', 0.0],
    'voc': [12, 'float', 0.0],
    'co2': [14, 'float', 0.0],
    'pm2.5': [16, 'float', 0.0],
    'time_stamp': [18, 'uint32', int(time.time())],
    'reserve': [0, 'unknow', 0]
}








class Setting:
    def __init__(self):
        self.sys_parameter_address = 4000 - 1
        self.sensor_module_num = 5
        self.sensors_address = [4021-1, 4051-1, 4081-1, 4111-1, 4141-1]



    def get_system_parameter_address_and_values(self):
        address_begin = self.sys_parameter_address
        values = []
        for i in System_Parameter:
            print(System_Parameter_Config[i])
            Convert.add_uint16_data(values, System_Parameter_Config[i][1], System_Parameter_Config[i][2])
        return address_begin,values


    def get_sensor_address_and_values(self, module_id):
        address_begin = self.sensors_address[module_id]
        sensor_config = deepcopy(Sensor_Config)
        sensor_config['module_id'][2] = module_id
        sensor_config['install_num'][2] = 'YTHA-' + str(module_id)
        values = []
        for i in sensor:
            print(sensor_config[i])
            Convert.add_uint16_data(values, sensor_config[i][1], sensor_config[i][2])
        return address_begin,values




if __name__ == '__main__':
    s = Setting()
    for i in range(5):
        print(s.get_sensor_address_and_values(1))
