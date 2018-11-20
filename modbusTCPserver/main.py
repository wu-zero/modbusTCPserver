from queue import Queue
from threading import Timer

from Consumer_CommandSolve import Consumer_CommandSolve
from MyModbusServer import MyModbusServer
from MySerial import MySerial
from Producer_Console import Producer_Console
from Producer_SerialPort import Producer_Serial
from SensorModuleMonitor import SensorModuleMonitor

if __name__ == '__main__':
    my_serial = MySerial()
    my_modbus_server = MyModbusServer()
    my_monitor = SensorModuleMonitor()

    def routine_fun():
        my_modbus_server.updata_system_timestamp()
        my_monitor.monitor()
        t = Timer(0.5, routine_fun)
        t.start()

    routine = Timer(0.5, routine_fun)
    routine.start()

    queue = Queue()  # 队列实例化

    producer_serial_port = Producer_Serial('serial_port', queue, my_serial)  # 调用对象，并传如参数线程名、实例化队列
    producer_console = Producer_Console('console', queue)
    consumer = Consumer_CommandSolve('solve', queue, my_modbus_server, my_serial, my_monitor)

    producer_serial_port.start()  # 开始制造
    producer_console.start()  # 开始制造
    consumer.start()  # 开始消费

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
