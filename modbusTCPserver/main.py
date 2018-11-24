from queue import Queue
from threading import Timer

from Consumer_CommandSolve import Consumer_CommandSolve
from MyModbusServer import MyModbusServer
from MySerial import MySerial
from Producer_Console import Producer_Console
from Producer_SerialPort import Producer_Serial
from SensorModuleMonitor import SensorModuleMonitor


if __name__ == '__main__':
    #  队列实例化
    queue = Queue()
    #  ZigBee串口
    my_serial = MySerial()
    #  modbusTCPserver
    my_modbus_server = MyModbusServer(queue)
    #  数据流监控
    my_monitor = SensorModuleMonitor()

    #  定义系统定时执行函数
    def sys_routine_fun():
        #  定时更新系统时间戳
        my_modbus_server.updata_system_timestamp()
        #  定时监控传感器模块
        my_monitor.monitor_modules()
        t = Timer(0.5, sys_routine_fun)
        t.start()
    #  启动系统定时执行函数
    routine = Timer(0.5, sys_routine_fun)
    routine.start()

    #  串口(生产者)、命令行(生产者)、命令处理(消费者)
    producer_serial_port = Producer_Serial('serial_port', queue, my_serial)
    producer_console = Producer_Console('console', queue)
    consumer = Consumer_CommandSolve('solve', queue, my_modbus_server, my_serial, my_monitor)

    producer_serial_port.start()  # 开始制造
    producer_console.start()  # 开始制造
    consumer.start()  # 开始消费

    #  只要有一个线程出错退出就退出主函数，程序重新自启
    while True:
        routine.join(0.1)
        producer_serial_port.join(0.1)
        producer_console.join(0.1)
        consumer.join(0.1)

        if producer_serial_port.isAlive() and producer_console.isAlive(
        ) and consumer.isAlive():
            continue
        else:
            print(producer_serial_port.isAlive(), producer_console.isAlive(), consumer.isAlive())

            my_modbus_server.close()

            import os
            import signal
            main_pid = os.getppid()
            print(main_pid)
            os.kill(os.getpid(), signal.SIGKILL)
            break

    print("main end")
