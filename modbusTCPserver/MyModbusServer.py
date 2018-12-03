import pickle
import modbus_tk.defines as cst
from modbus_tk import hooks, modbus_tcp

import Setting
import utils.SetPiTime as SetPiTime

SLAVE_ID = 1
PORT = 502
SYS_ANALOG_INPUTS_BLOCK_NAME = 'b1'
SYS_HOLDING_REGISTERS_BLOCK_NAME = 'b2'
HIDDEN_HOLDING_REGISTERS_BLOCK_NAME = 'b3'

SYS_ANALOG_INPUTS_BLOCK_ADDRESS = Setting.SYS_ANALOG_INPUTS_BLOCK_ADDRESS
SYS_HOLDING_REGISTERS_BLOCK_ADDRESS = Setting.SYS_HOLDING_REGISTERS_BLOCK_ADDRESS


save_file = '../data/save.data'


class MyModbusServer:
    """自定义modbusServer类
    """

    def __init__(self, queue):
        # 初始化
        try:
            self.queue = queue
            self.server, self.slave = self._init_modbus()
            print("server创建成功")
        except Exception as err:
            print("server创建失败，程序终止")
            print(err)
            # 程序退出
            import os
            import signal
            main_pid = os.getppid()
            print(main_pid)
            os.kill(os.getpid(), signal.SIGKILL)
        else:
            self._init_system_parameter_and_sensor_modules()
            print("running......")

    # ====================modbus底层====================
    def _init_modbus(self, ):
        """modbusServer初始化
        
        Returns:
            server -- server服务器
            slave -- 从机
        """

        # 钩子
        hooks.install_hook('modbus.Slave.handle_write_multiple_registers_request',
                           self._handle_write_multiple_registers_request)
        hooks.install_hook('modbus.Slave.handle_write_single_register_request',
                           self._handle_write_single_registers_request)

        # 初始化
        server = modbus_tcp.TcpServer(address='0.0.0.0', port=PORT)

        # 服务启动
        server.start()

        # 建立从机
        slave = server.add_slave(SLAVE_ID)
        # 建立块
        # slave.add_block('0', cst.DISCRETE_INPUTS, 0, 100)
        # slave.add_block('0', cst.COILS, 0, 100)
        slave.add_block(SYS_ANALOG_INPUTS_BLOCK_NAME, cst.ANALOG_INPUTS, SYS_ANALOG_INPUTS_BLOCK_ADDRESS, 171)
        slave.add_block(SYS_HOLDING_REGISTERS_BLOCK_NAME, cst.HOLDING_REGISTERS, SYS_HOLDING_REGISTERS_BLOCK_ADDRESS, 6)
        # slave.add_block(HIDDEN_HOLDING_REGISTERS_BLOCK_NAME, cst.HOLDING_REGISTERS, 5999, 20)

        return server, slave

    def _set_analog_inputs_values(self, address_begin, values):
        """写modbus analog_inputs寄存器
        
        Arguments:
            address_begin {int} -- 寄存器起始位置
            values {list of uint16} -- 要写入的数据
        """

        self.slave.set_values(SYS_ANALOG_INPUTS_BLOCK_NAME, address_begin, values)

    def _get_analog_inputs_values(self, address_begin, length):
        """写modbus analog_inputs寄存器
        
        Arguments:
            address_begin {int} -- 寄存器起始位置
            length {int} -- 要读取的长度
        
        Returns:
            list of uint16 -- 读取到的数据
        """

        return self.slave.get_values(SYS_ANALOG_INPUTS_BLOCK_NAME, address_begin, length)

    def _set_holding_registers_values(self, address_begin, values):
        """写系统设置数据(modbus holding寄存器)
        
        Arguments:
            address_begin {int} -- 寄存器起始位置
            values {list of uint16} -- 要写入的数据
        """

        self.slave.set_values(SYS_HOLDING_REGISTERS_BLOCK_NAME, address_begin, values)

    def _get_holding_registers_values(self, address_begin, length):
        """读系统设置数据(modbus holding寄存器)
        
        Arguments:
            address_begin {int} -- 寄存器起始位置
            length {int} -- 要读取的长度
        
        Returns:
            list of uint16 -- 读取到的数据
        """

        return self.slave.get_values(SYS_HOLDING_REGISTERS_BLOCK_NAME, address_begin, length)

    def close(self):
        """结束server
        """

        self.server.stop()

    # ======================modbus底层 hook相关=================
    #  处理写single数据事件
    def _handle_write_single_registers_request(self, request_data_from_hook):
        slave, bytes_data = request_data_from_hook
        #  获取地址和数据(uint16）
        address, values = Setting.solve_single_request(bytes_data)

        #  进行处理
        if address in [Setting.Pi_Time_stamp_Address, Setting.Pi_Time_stamp_Address+1]:
            values_old = self._get_holding_registers_values(Setting.Pi_Time_stamp_Address, 2)
            if address == Setting.Pi_Time_stamp_Address and len(values) == 1:
                time_stamp = values[0] + values_old[1] * 2 ** 16
                SetPiTime.linux_set_time(time_stamp)
                print(time_stamp)
            elif address == Setting.Pi_Time_stamp_Address + 1 and len(values) == 1:
                time_stamp = values_old[0] + values[0] * 2 ** 16
                SetPiTime.linux_set_time(time_stamp)
                print(time_stamp)
        else:
            pass

    #  处理写multiple数据事件
    def _handle_write_multiple_registers_request(self, request_data_from_hook):
        slave, bytes_data = request_data_from_hook
        # 获取地址和数据(uint16）
        address, values = Setting.solve_multiple_request(bytes_data)

        #  进行处理
        if address in [Setting.Pi_Time_stamp_Address, Setting.Pi_Time_stamp_Address+1]:
            values_old = self._get_holding_registers_values(Setting.Pi_Time_stamp_Address, 2)
            if address == Setting.Pi_Time_stamp_Address and len(values) == 2:
                time_stamp = values[0] + values[1] * 2 ** 16
                SetPiTime.linux_set_time(time_stamp)
                print(time_stamp)
            elif address == Setting.Pi_Time_stamp_Address and len(values) == 1:
                time_stamp = values[0] + values_old[1]*2**16
                SetPiTime.linux_set_time(time_stamp)
                print(time_stamp)
            elif address == Setting.Pi_Time_stamp_Address+1 and len(values) == 1:
                time_stamp = values_old[0] + values[0]*2**16
                SetPiTime.linux_set_time(time_stamp)
                print(time_stamp)
        elif address == Setting.Extern_Zigbee_Address_Address and len(values) == 4:
            extern_address = values[0] + values[1] * 2**16 + values[2] * 2**32 + values[3] * 2**48

            # 写入队列编号
            self.queue.put(['set extern address', extern_address])

        # elif address == Setting.Hidden_Address and len(values) == 13:
        #     address_begin = Setting.get_sensor_address(values[0])
        #     values = values[1:]
        #     self.__set_analog_inputs_values(address_begin, values)
        else:
            pass


    #  =====================初始化===========================
    def _init_system_parameter(self):
        """系统参数数据初始化,通过定义
        """

        address_begin, values = Setting.get_system_parameter_address_and_values()
        self._set_analog_inputs_values(address_begin, values)
        print("system_parameter初始化成功")

    def _init_sensor_modules(self):
        """传感器模块初始化，通过定义
        """

        for module_id in Setting.Sensor_Module_Id_List:
            address_begin, values = Setting.get_sensor_address_and_values(module_id)
            self._set_analog_inputs_values(address_begin, values)
        print("sensors_parameter初始化成功")

    def _init_all_data_from_file(self):
        try:
            f = open(save_file, 'rb')
            data_dict = pickle.load(f)
            f.close()
            data1 = data_dict['input_block_data']
            data2 = data_dict['hold_block_data']
            if len(data1) == 171 and len(data2) == 6:
                self._set_analog_inputs_values(SYS_ANALOG_INPUTS_BLOCK_ADDRESS, data1)
                self._set_holding_registers_values(SYS_HOLDING_REGISTERS_BLOCK_ADDRESS, data2)
            else:
                raise Exception
        except Exception:
           raise Exception
        else:
           print("system_parameter初始化成功")
           print("sensors_parameter初始化成功")
           return True

    def _init_system_parameter_and_sensor_modules(self):
        """传感器模块数据初始化
        """

        try:
            self._init_all_data_from_file()
            print('从文件初始化数据')
        except Exception:
            print('从定义初始化数据')
            self._init_system_parameter()
            self._init_sensor_modules()
        finally:
            print('modbus数据初始化成功')

    #  =====================应用===========================
    #  更新时间戳
    def update_system_timestamp(self):
        address_begin, values = Setting.get_timestamp_address_and_values()
        self._set_analog_inputs_values(address_begin, values)
        address_begin, values = Setting.get_Pi_timestamp_address_and_values()
        self._set_holding_registers_values(address_begin, values)

    #  更新传感器模块数据
    def update_sensor_module(self, bytes_data):
        address_begin, values = Setting.get_address_and_values_from_bytes(bytes_data)
        self._set_analog_inputs_values(address_begin, values)

    def save_all_data_from_modbus(self):
        """从modbusServer读所有数据,存储起来,用于文件初始化方式
        """

        input_block_data = self._get_analog_inputs_values(SYS_ANALOG_INPUTS_BLOCK_ADDRESS, 171)
        hold_block_data = self._get_holding_registers_values(SYS_HOLDING_REGISTERS_BLOCK_ADDRESS, 6)
        block_data_now = {'input_block_data': input_block_data, 'hold_block_data': hold_block_data}
        with open(save_file, 'wb') as f:
            pickle.dump(block_data_now, f)


if __name__ == "__main__":
    from queue import Queue
    queue = Queue()
    mymodbus = MyModbusServer(queue)
    mymodbus.update_system_timestamp()
    while True:
       pass
       
