import numpy as np
import struct

# float转换为2进制
def float_to_bin(num):
    bits, = struct.unpack('I',struct.pack('f',num))
    return "{:032b}".format(bits)


# float转换为两个16位
def float_to_uint16(num):
    number_bytes = struct.pack('f',num)
    bits_low, = struct.unpack('H',number_bytes[0:2])
    bits_high, = struct.unpack('H', number_bytes[2:4])
    # print("float":float_to_bin(num))
    # print("低16位：{:016b}".format(bits_low))
    # print("高16位：{:016b}".format(bits_high))
    return [bits_low,bits_high]


# uint32转换为两个16位
def uint32_to_uint16(num):
    number_bytes = struct.pack('I',num)
    bits_low, = struct.unpack('H',number_bytes[0:2])
    bits_high, = struct.unpack('H', number_bytes[2:4])
    # print("uint32:{:032b}".format(num))
    # print("低16位：{:016b}".format(bits_low))
    # print("高16位：{:016b}".format(bits_high))
    return [bits_low,bits_high]


# char10转换为五个16位
def char10_to_uint16(string):

    types = [0 for i in range(10)]
    result = [0 for i in range(10)]
    for i in range(min(10, len(string))):
        types[i] = ord(string[i])
    for i in range(5):
        result[i] = types[i*2] * 256 + types[i*2+1]
    # print("types:",types)
    # print("result",result)
    return result

# 2字节转换为n个16位
def byte2_to_uint16(bytes):
    result, = struct.unpack('H', bytes[0:2])
    return [result]


# n字节转换为n/2个16位
def bytes_to_uint16(bytes):
    bytes_num = len(bytes)
    uint16_num = bytes_num//2
    result = []
    for i in range(uint16_num):
        result.append(byte2_to_uint16(bytes[i * 2:i * 2 + 2])[0])
    return result


def add_data(result=None, data_type=None, data=None):
    if result is None or data_type is None or data is None:
        print('error')
    else:
        if data_type == 'uint16':
            result.append(data)
        elif data_type == 'uint32':
            data_convert = uint32_to_uint16(data)
            for i in data_convert:
                result.append(i)
        elif data_type == 'float':
            data_convert = float_to_uint16(data)
            for i in data_convert:
                result.append(i)
        elif data_type == 'char*10':
            data_convert = char10_to_uint16(data)
            for i in data_convert:
                result.append(i)
        elif data_type == 'bytes':
            data_convert = bytes_to_uint16(data)
            for i in data_convert:
                result.append(i)
        else:
            pass


if __name__ == '__main__':

    print(char10_to_uint16('aaaaa'))
    float_to_uint16(1.1)
    uint32_to_uint16(65535)
    print(byte2_to_uint16(b'ab'))
    bytes_to_uint16(b'abababab\0\0')
    print("--------------------")

    result = [1]
    print(result)
    add_data(result,'uint16',2)
    print(result)
    add_data(result, 'uint32', 65535)
    print(result)
    add_data(result, 'uint32', 65536)
    print(result)
    add_data(result, 'char*10', 'a')
    print(result)
    add_data(result, 'bytes', b'\0\0\0a\0baba\0b\0')
    print(result)
