from queue import Queue
from threading import Timer
import time
from MySerial import MySerial
from MyModbus import MyModbus
from Producer_Console import Producer_Console
from Consumer_CommandSolve import Consumer_CommandSolve
from Producer_SerialPort import Producer_Serial
from SensorModuleMonitor import SensorModuleMonitor



if __name__ == '__main__':
    my_serial = MySerial()
    my_modbus = MyModbus()
    my_monitor = SensorModuleMonitor()

    def routine_fun():
        my_modbus.updata_system_timestamp()
        my_monitor.monitor()
        t = Timer(0.5, routine_fun)
        t.start()

    routine = Timer(0.5, routine_fun)
    routine.start()
    routine.join()
    print('系统维护线程开始执行', time.time())

    queue = Queue()  # 队列实例化

    producer_serial_port = Producer_Serial('serial_port', queue, my_serial)  # 调用对象，并传如参数线程名、实例化队列
    producer_console = Producer_Console('console', queue)
    consumer = Consumer_CommandSolve('solve', queue, my_modbus, my_serial, my_monitor)

    producer_serial_port.start()  # 开始制造
    producer_console.start()  # 开始制造
    consumer.start()  # 开始消费

    producer_serial_port.join()
    producer_console.join()
    consumer.join()











