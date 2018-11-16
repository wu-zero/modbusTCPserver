import struct


# float转换为2进制
def _float_to_bin(number):
    number_bytes, = struct.unpack('I', struct.pack('f', number))
    return "{:032b}".format(number_bytes)


# float转换为两个16位
def float_to_uint16(number):
    number_bytes = struct.pack('f', number)
    bits_low, = struct.unpack('H',number_bytes[0:2])
    bits_high, = struct.unpack('H', number_bytes[2:4])
    # print("float":float_to_bin(num))
    # print("低16位：{:016b}".format(bits_low))
    # print("高16位：{:016b}".format(bits_high))
    return [bits_low, bits_high]


# uint32转换为两个16位
def uint32_to_uint16(number):
    number_bytes = struct.pack('I', number)
    bits_low, = struct.unpack('H',number_bytes[0:2])
    bits_high, = struct.unpack('H', number_bytes[2:4])
    # print("uint32:{:032b}".format(num))
    # print("低16位：{:016b}".format(bits_low))
    # print("高16位：{:016b}".format(bits_high))
    return [bits_low, bits_high]


# char10转换为五个16位
def char10_to_uint16(string_number):
    number_bytes = [0 for i in range(10)]
    result = [0 for i in range(5)]
    for i in range(min(10, len(string_number))):
        number_bytes[i] = ord(string_number[i])
    for i in range(5):
        result[i] = number_bytes[i*2] * 256 + number_bytes[i*2+1]
    # print("types:",types)
    # print("result",result)
    return result


# 2字节转换为一个16位
def byte2_to_uint16(number_bytes, little_endian=True):
    if little_endian:
        result, = struct.unpack('H', number_bytes[0:2])
    else:
        result, = struct.unpack('!H', number_bytes[0:2])
    return result
    ############方法二    速度慢淘汰
    # result = int.from_bytes(number_bytes[0:2], byteorder='little')
    # return result


def byte4_to_uint32(number_bytes, little_endian=True):
    if little_endian:
        result, = struct.unpack('I', number_bytes[0:4])
    else:
        result, = struct.unpack('!I', number_bytes[0:4])
    return result
    ############方法二    速度慢淘汰
    # result = int.from_bytes(number_bytes[0:4], byteorder='little')
    # return result


def byte4_to_float(number_bytes):
    result, = struct.unpack('f', number_bytes[0:4])
    return result


# n字节转换为n/2个16位
def bytes_to_uint16(number_bytes):
    bytes_num = len(number_bytes)
    uint16_num = bytes_num//2
    result = []
    for i in range(uint16_num):
        result.append(byte2_to_uint16(number_bytes[i * 2:i * 2 + 2]))
    return result

# real data to modbus data
def convert_to_uint16_data(result=None, data_type=None, data=None):
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

# serial to real data
def convert_to_real_data(result=None, data_type=None, data=None):
    if result is None or data_type is None or data is None:
        print('error')
    else:
        if data_type == 'uint16':
            result.append(byte2_to_uint16(data))
        elif data_type == 'uint32':
            result.append(byte4_to_uint32(data))
        elif data_type == 'float':
            result.append(byte4_to_float(data))
        elif data_type == 'char*10':
            pass
        elif data_type == 'bytes':
            pass
        else:
            pass


if __name__ == '__main__':

    # print(char10_to_uint16('aaaaa'))
    # float_to_uint16(1.1)
    # uint32_to_uint16(65535)
    # print(byte2_to_uint16(b'ab'))
    # bytes_to_uint16(b'abababab\0\0')
    # print("--------------------")
    #
    # result = [1]
    # print(result)
    # convert_to_uint16_data(result, 'uint16', 2)
    # print(result)
    # convert_to_uint16_data(result, 'uint32', 65535)
    # print(result)
    # convert_to_uint16_data(result, 'uint32', 65536)
    # print(result)
    # convert_to_uint16_data(result, 'char*10', 'a')
    # print(result)
    # convert_to_uint16_data(result, 'bytes', b'\0\0\0a\0baba\0b\0')
    # print(result)
    #
    result = []
    # print(result)
    # convert_to_real_data(result, 'uint16', b'qq')
    # print(result)
    convert_to_real_data(result, 'uint32', b'n\xdf\xe6[')
    print(result)
    # print(result)
    # convert_to_real_data(result, 'float', b'qqqqqqqq')
    # print(result)
    # convert_to_real_data(result, 'char*10', 'a')
    # print(result)
    # convert_to_real_data(result, 'bytes', b'\0\0\0a\0baba\0b\0')
    # print(result)
    # starttime = datetime.datetime.now()
    # for i in range(10000000):
    #     byte2_to_uint16(b'a1')
    # endtime = datetime.datetime.now()
    # print((endtime - starttime).seconds)
    #print(byte2_to_uint16(b'\x13\x87', little_endian=False))
    #print(byte4_to_uint32(b'\xb0Z[\xeb'))
