#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""
 Modbus TestKit: Implementation of Modbus protocol in python
 (C)2009 - Luc Jean - luc.jean@gmail.com
 (C)2009 - Apidev - http://www.apidev.fr
 This is distributed under GNU LGPL license, see license.txt
"""
# Discrete Inputs   1-65534   bool
# Coils             1-65534   bool
# Input Registers   1-65534   32767
# Hoding Registers  1-65534   32767

import sys

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
from modbus_tk.exceptions import(
    ModbusError, ModbusFunctionNotSupportedError, DuplicatedKeyError, MissingKeyError, InvalidModbusBlockError,
    InvalidArgumentError, OverlapModbusBlockError, OutOfModbusBlockError, ModbusInvalidResponseError,
    ModbusInvalidRequestError
)




def main():
    """main"""

    logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")

    try:
        #Create the server
        server = modbus_tcp.TcpServer(address='0.0.0.0', port=502)
        logger.info("running...")
        logger.info("enter 'quit' for closing the server")
        # 服务启动
        server.start()
        # 建立从机
        slave_1 = server.add_slave(1)
        # 建立块
        slave_1.add_block('b1', cst.DISCRETE_INPUTS, 0, 100)
        slave_1.add_block('b2', cst.COILS, 0, 100)
        slave_1.add_block('b3', cst.ANALOG_INPUTS, 0, 100)
        slave_1.add_block('b4', cst.HOLDING_REGISTERS, 0, 100)

        while True:
            cmd = sys.stdin.readline()
            args = cmd.split(' ')

            if cmd.find('quit') == 0:
                sys.stdout.write('bye-bye\r\n')
                break

            # 添加slave从机
            elif args[0] == 'add_slave':
                slave_id = int(args[1])
                try:
                    server.add_slave(slave_id)
                except DuplicatedKeyError as err:
                    sys.stdout.write(str(err)+'\r\n')
                except Exception as err:
                    sys.stdout.write(str(err)+',plase make sure 0 <= slave_id < 255\r\n ')
                else:
                    sys.stdout.write('done: slave %d added\r\n' % slave_id)

            # 添加block块
            elif args[0] == 'add_block':

                slave_id = int(args[1])
                name = args[2]
                block_type = int(args[3])
                starting_address = int(args[4])
                length = int(args[5])


                try:
                    slave = server.get_slave(slave_id)
                except MissingKeyError as err:
                    sys.stdout.write(str(err)+'\r\n')
                else:
                    try:
                        slave.add_block(name, block_type, starting_address, length)
                    except Exception as err:
                        sys.stdout.write(str(err)+'\r\n')
                    else:
                        sys.stdout.write('done: block %s added\r\n' % name)


            # 设定值
            elif args[0] == 'set_values':

                slave_id = int(args[1])
                name = args[2]
                address = int(args[3])
                values = []
                for val in args[4:]:
                    values.append(val)# int

                try:
                    slave = server.get_slave(slave_id)
                except MissingKeyError as err:
                    sys.stdout.write(str(err) + '\r\n')
                else:
                    try:
                        slave.set_values(name, address, values)
                    except Exception as err:
                        sys.stdout.write(str(err) + '\r\n')
                    else:
                        values = slave.get_values(name, address, len(values))
                        sys.stdout.write('done: values written: %s\r\n' % str(values))


            elif args[0] == 'get_values':
                slave_id = int(args[1])
                name = args[2]
                address = int(args[3])
                length = int(args[4])
                try:
                    slave = server.get_slave(slave_id)
                except MissingKeyError as err:
                    sys.stdout.write(str(err) + '\r\n')
                else:
                    try:
                        values = slave.get_values(name, address, length)
                    except Exception as err:
                        sys.stdout.write(str(err) + '\r\n')
                    else:
                        sys.stdout.write('done: values read: %s\r\n' % str(values))

            else:
                sys.stdout.write("unknown command %s\r\n" % args[0])
    finally:
        server.stop()


if __name__ == "__main__":
    main()