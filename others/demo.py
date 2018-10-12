import Convert
import time
data_type_all = ('uint16','uint32','float','string')
# 地址相关
modules = \
    {'system_parameter': 4000,
        'sensor1': 4021,
        'sensor2': 4051,
        'sensor3': 4081,
        'sensor4': 4111,
        'sensor5': 4141}

system_parameter = \
    {'version_num': [0, 'uint16'],
        'unit_num': [1, 'uint16'],
        'sensor_num': [2, 'uint16'],
        'time_stamp': [3, 'uint32'],
        'reserve': [5, 'unknow']}

sensor_modules = \
    {'module_num': [0,'uint16'],
        'install_num': [1,'string'],
        'temperature': [6,'float'],
        'humiditu': [8,'float'],
        'o3': [10,'float'],
        'voc': [12,'float'],
        'co2': [14,'float'],
        'pm2.5': [16,'float'],
        'time_stamp': [18,'uint32'],
        'reserve': [20,'unknow']}

# 值相关
# modules_value= \
#     {'system_parameter': 4000,
#         'sensor1': 4021,
#         'sensor2': 4051,
#         'sensor3': 4081,
#         'sensor4': 4111,
#         'sensor5': 4141}
system_parameter_value = \
    {'version_num': 1,
        'unit_num': 1,
        'sensor_num': 5,
        'time_stamp': int(time.time()),
        'reserve': 0}

sensor_value = \
    {'module_num': 1,
        'install_num': 'YTHA-7',
        'temperature': 0.0,
        'humiditu': 0.0,
        'o3': 0.0,
        'voc': 0.0,
        'co2': 0.0,
        'pm2.5': 0.0,
        'time_stamp': int(time.time()),
        'reserve': 0}


def set_values(address_begin, value, data_type):

    if data_type in data_type_all:
        if data_type == 'uint16':
            address_num = 1
            value_new = [value]
        elif data_type == 'uint32':
            address_num = 2
            value_new = Convert.uint32_to_uint16(value)
        elif data_type == 'float':
            address_num = 2
            value_new = Convert.float_to_uint16(value)
        elif data_type == 'string':
            address_num = 5
            value_new = Convert.char10_to_uint16(value)
        for i in range(address_num):
            print(address_begin+i,value_new[i])

    else:
        print('wrong')

def updata(data):
    if data[0] == 0:
        begin_address = modules['sensor1']
        print('updata'+'sensor1')





if __name__ == '__main__':
    set_values(1000,'aaa','string')
    print(int(time.time()))
    data = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    updata(data)