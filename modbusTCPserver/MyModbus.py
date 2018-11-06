import sys
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp


import Setting


SLAVE_ID = 1
PORT = 502
BLOCK_NAME = 'b1'


class MyModbus:

    def __init__(self):    
        # 初始化
        try:
            self.server, self.slave = self.__init_modbus()
            print("server创建成功")
            self.__init_system_parameter()
            self.__init_sensors()
            print("running......")
        except Exception as err:
            print("server创建失败，程序终止")
            print(err)
            sys.exit()

    # 更新时间戳
    def updata_system_timestamp(self):
        address_begin, values = Setting.get_timestamp_address_and_values()
        self.__set_values(address_begin, values)

    def updata_sensor_module(self, data_bytes):
        address_begin, values = Setting.get_address_and_values_from_bytes(data_bytes)
        self.__set_values(address_begin, values)

    # modbus初始化
    @staticmethod
    def __init_modbus():
        server = modbus_tcp.TcpServer(address='0.0.0.0', port=PORT)
        # 服务启动
        server.start()
        # 建立从机
        slave = server.add_slave(SLAVE_ID)
        # 建立块
        # slave.add_block('b1', cst.DISCRETE_INPUTS, 0, 100)
        # slave.add_block('b2', cst.COILS, 0, 100)
        slave.add_block(BLOCK_NAME, cst.ANALOG_INPUTS, 3999, 4169)
        # slave.add_block('b4', cst.HOLDING_REGISTERS, 0, 100)
        return server, slave

    # 系统参数初始化
    def __init_system_parameter(self):
        address_begin, values = Setting.get_system_parameter_address_and_values()
        self.__set_values(address_begin,values)
        print("system_parameter初始化成功")

    # 传感器模块初始化
    def __init_sensors(self):
        for module_id in Setting.Sensor_Module_Id_List:
            address_begin, values = Setting.get_sensor_address_and_values(module_id)
            self.__set_values(address_begin, values)
        print("sensors_parameter初始化成功")

    # =======================modbus底层=================
    # 设置modbus寄存器数据
    def __set_values(self, address_begin, values):
        if address_begin is not None:
            self.slave.set_values(BLOCK_NAME, address_begin, values)


if __name__ == "__main__":
    mymodbus = MyModbus()
    mymodbus.updata_system_timestamp()
    while True:
       pass