import time
from copy import deepcopy
import Convert

# ===================================================协议
Sys_Parameter_Address = 4000 - 1
Sensor_Module_Id_List = [1, 2, 3, 4, 5]
Sensor_Module_Address_Dict = {1: 4021 - 1, 2: 4051 - 1, 3: 4081 - 1, 4: 4111 - 1, 5: 4141 - 1}

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
Sensor_Module = [
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
Sensor_Module_Config = {
    'module_id': [0, 'uint16', 1],
    'install_num': [1, 'char*10', 'YTHA-7'],
    'temperature': [6, 'float', 0.0],
    'humidity': [8, 'float', 0.0],
    'o3': [10, 'float', 0.0],
    'voc': [12, 'float', 0.0],
    'co2': [14, 'float', 0.0],
    'pm2.5': [16, 'float', 0.0],
    'time_stamp': [18, 'uint32', int(time.time())],
    'reserve': [20, 'unknow', 0]
}

# ====================================================ZigBee串口
SERIAL_ADDRESS = '/dev/ttyS0'

# ====================================================log
CONSOLE_LOG_FLAG = False


def get_serial_address():
    return SERIAL_ADDRESS



def get_system_parameter_address_and_values():
    address_begin = Sys_Parameter_Address
    values = []
    for i in System_Parameter:
        #print(System_Parameter_Config[i])
        Convert.add_uint16_data(values, System_Parameter_Config[i][1], System_Parameter_Config[i][2])
    return address_begin, values


def get_sensor_address_and_values(module_id):
    if module_id in Sensor_Module_Id_List:
        address_begin = Sensor_Module_Address_Dict[module_id]
        sensor_config = deepcopy(Sensor_Module_Config)
        sensor_config['module_id'][2] = module_id
        sensor_config['install_num'][2] = 'YTHA-' + str(module_id)
        values = []
        for i in Sensor_Module:
            #print(sensor_config[i])
            Convert.add_uint16_data(values, sensor_config[i][1], sensor_config[i][2])
        return address_begin,values
    else:
        pass


def get_timestamp_address_and_values():
    address_begin = Sys_Parameter_Address + System_Parameter_Config['time_stamp'][0]
    values = []
    Convert.add_uint16_data(values, System_Parameter_Config['time_stamp'][1], int(time.time()))
    return address_begin, values


def get_sensor_address(module_id):
    if module_id in Sensor_Module_Id_List:
        address_begin = Sensor_Module_Address_Dict[module_id] + Sensor_Module_Config['temperature'][0]
        return address_begin
    else:
        return None

#  解析zigbee接收到的数据
def get_real_data(data):
    data_module_num = data[:2]
    data_others = data[2:]
    values = []
    # 添加module_num
    Convert.add_real_data(values, Sensor_Module_Config['module_id'][1], data_module_num)
    # 添加数据
    for sensor_module_part in Sensor_Module[2:]:
        #print(data_others[(Sensor_Module_Config[sensor_module_part][0]-6)*2:])
        Convert.add_real_data(values,Sensor_Module_Config[sensor_module_part][1],data_others[(Sensor_Module_Config[sensor_module_part][0]-6)*2:])
    return values


if __name__ == '__main__':
    print(get_real_data(b'\0\0cdefglskjdfdsddddewwwwwwwwww\r\n'))
    pass
