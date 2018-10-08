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
    print(float_to_bin(num))
    print("低16位：{:016b}".format(bits_low))
    print("高16位：{:016b}".format(bits_high))

    return [bits_low,bits_high]

# uint32转换为两个16位
def uint32_to_uint16(num):
    number_bytes = struct.pack('!I',num)
    bits_high, = struct.unpack('!H',number_bytes[0:2])
    bits_low, = struct.unpack('!H', number_bytes[2:4])
    print("{:032b}".format(num))
    print("低16位：{:016b}".format(bits_low))
    print("高16位：{:016b}".format(bits_high))
    return [bits_low,bits_high]


# string转换为五个16位
def string_to_uint16(string):
    result = np.zeros([5],dtype=np.uint16)

    for i in range(min(5,len(string))):
        result[i] = ord(string[i])
    print(string)
    print(result)
    return result

if __name__ == '__name__':

    string_to_uint16('abc')