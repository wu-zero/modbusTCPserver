def crc16(bytes_data, bytes_num):
    crc = 0xffff
    i = 0
    for i in range(bytes_num):
        crc = crc ^ bytes_data[i]
        for j in range(8):
            if crc & 0x01:
                crc = crc >> 1
                crc = crc ^ 0xa001
            else:
                crc = crc >> 1
    return crc.to_bytes(2, byteorder='little')


if __name__ == '__main__':
    print(crc16(b'\xaa\x05\x00\x1f\x85\\B{\x14]B\xaeG]B\x85\xeb]Bq=^B\xd7\xa3^B\xd5\xdd\x00\x00', 31))
