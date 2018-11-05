from queue import Queue


from MySerial import MySerial
from MyModbus import MyModbus
from Producer_Console import Producer_Console
from Consumer_CommandSolve import Consumer_CommandSolve
from Producer_SerialPort import Producer_Serial




if __name__ == '__main__':
    my_serial = MySerial()
    my_modbus = MyModbus()


    queue = Queue()  # 队列实例化
    producer_serial_port = Producer_Serial('serial_port', queue, my_serial)  # 调用对象，并传如参数线程名、实例化队列
    producer_console = Producer_Console('console', queue)
    consumer = Consumer_CommandSolve('solve', queue, my_modbus, my_serial)  # 同上，在制造的同时进行消费

    producer_serial_port.start()  # 开始制造
    producer_console.start()  # 开始制造
    consumer.start()  # 开始消费
    """
    join（）的作用是，在子线程完成运行之前，这个子线程的父线程将一直被阻塞。
　　join()方法的位置是在for循环外的，也就是说必须等待for循环里的两个进程都结束后，才去执行主进程。
    """
    producer_serial_port.join()
    producer_console.join()
    consumer.join()
