import modbus_tk.defines as cst
from modbus_tk import hooks, modbus_tcp

import Setting
import utils.SetPiTime as SetPiTime

SLAVE_ID = 1
PORT = 502
SYS_ANALOG_INPUTS_BLOCK_NAME = 'b1'
SYS_HOLDING_REGISTERS_BLOCK_NAME = 'b2'
HIDDEN_HOLDING_REGISTERS_BLOCK_NAME = 'b3'


class MyModbusServer:

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
            self._init_system_parameter()
            self._init_sensor_modules()
            print("running......")

    # ====================modbus底层====================
    # modbus初始化
    def _init_modbus(self, ):
        # 钩子
        hooks.install_hook('modbus.Slave.handle_write_multiple_registers_request',
                           self.__handle_write_multiple_registers_request)
        hooks.install_hook('modbus.Slave.handle_write_single_register_request',
                           self.__handle_write_single_registers_request)

        # 初始化
        server = modbus_tcp.TcpServer(address='0.0.0.0', port=PORT)

        # 服务启动
        server.start()

        # 建立从机
        slave = server.add_slave(SLAVE_ID)
        # 建立块
        # slave.add_block('0', cst.DISCRETE_INPUTS, 0, 100)
        # slave.add_block('0', cst.COILS, 0, 100)
        slave.add_block(SYS_ANALOG_INPUTS_BLOCK_NAME, cst.ANALOG_INPUTS, 3999, 171)
        slave.add_block(SYS_HOLDING_REGISTERS_BLOCK_NAME, cst.HOLDING_REGISTERS, 4999, 6)
        # slave.add_block(HIDDEN_HOLDING_REGISTERS_BLOCK_NAME, cst.HOLDING_REGISTERS, 5999, 20)

        return server, slave

    # 写modbus analog_inputs寄存器
    def _set_analog_inputs_values(self, address_begin, values):
        self.slave.set_values(SYS_ANALOG_INPUTS_BLOCK_NAME, address_begin, values)

    # 写系统设置数据
    def _set_holding_registers_values(self, address_begin, values):
        self.slave.set_values(SYS_HOLDING_REGISTERS_BLOCK_NAME, address_begin, values)

    # 读系统设置数据
    def _get_holding_registers_values(self, address_begin, length):
        return self.slave.get_values(SYS_HOLDING_REGISTERS_BLOCK_NAME, address_begin, length)

    # =======================结束server=================
    def close(self):
        self.server.stop()

    #  =====================应用===========================

    # 系统参数初始化
    def _init_system_parameter(self):
        address_begin, values = Setting.get_system_parameter_address_and_values()
        self._set_analog_inputs_values(address_begin, values)
        print("system_parameter初始化成功")

    # 传感器模块初始化
    def _init_sensor_modules(self):
        for module_id in Setting.Sensor_Module_Id_List:
            address_begin, values = Setting.get_sensor_address_and_values(module_id)
            self._set_analog_inputs_values(address_begin, values)
        print("sensors_parameter初始化成功")

    #  更新时间戳
    def updata_system_timestamp(self):
        address_begin, values = Setting.get_timestamp_address_and_values()
        self._set_analog_inputs_values(address_begin, values)
        address_begin, values = Setting.get_Pi_timestamp_address_and_values()
        self._set_holding_registers_values(address_begin, values)

    #  更新传感器模块数据
    def updata_sensor_module(self, bytes_data):
        address_begin, values = Setting.get_address_and_values_from_bytes(bytes_data)
        self._set_analog_inputs_values(address_begin, values)

    # =======================modbus底层 hook相关=================
    #  处理写single数据事件
    def __handle_write_single_registers_request(self, request_data_from_hook):
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
    def __handle_write_multiple_registers_request(self, request_data_from_hook):
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


if __name__ == "__main__":
    from queue import Queue
    queue = Queue()
    mymodbus = MyModbusServer(queue)
    mymodbus.updata_system_timestamp()
    while True:
       pass
       
