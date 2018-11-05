####事件驱动的红绿灯实例####
import threading
import time


class traffic(threading.Thread):
    '''使用继承类方式写一个进程'''
    def __init__(self,event_obj):
        threading.Thread.__init__(self)
        self.event_obj = event_obj          # 传递事件对象

    def light(self):
        sec = 1         # 秒数
        while True:
            if sec / 1 == 1:                # 初始绿灯
                self.event_obj.set()        # 设置事件标志
                print ('green...')
            elif sec / 5 == 1:              # 计数5秒，变黄灯，黄灯可以通行，所以不改变事件标志
                print ('yellow...')
            elif sec / 7 == 1:              # 计数7秒，变红灯
                self.event_obj.clear()      # 清除事件标志
                print('red...')
            elif sec == 10:                 # 到10秒重新计数
                sec = 1
                continue
            sec += 1
            time.sleep(1)                   # 延迟

    def run(self):
        # 重写run函数，启动灯。
        self.light()

def car(event_obj):
    # 汽车通行函数
    while True:
        if event_obj.isSet():               # 判断事件标志是True，代表绿灯，打印通行
            print('the car is running!')
        else:                               # 判断事件标志是False，代表红灯，打印通行
            print('the car is stop!')
        time.sleep(1)                       # 延迟

def exit():
    # 定义控制函数，检测鼠标输入，C则结束所有进程，退出程序
    t = traffic(e)                                  # 创建信号灯线程对象
    c = threading.Thread(target=car, args=(e,))     # 创建汽车线程对象
    t.setDaemon(True)                               # 把两个设置成守护线程，跟随exit结束
    c.setDaemon(True)
    t.start()                                       # 线程启动
    c.start()
    while True:                                    # 循环检测键盘输入
        s = input().strip()                         # 读取键盘输入字符
        if s == 'c':                               # 如果为C，结束exit
            print('程序退出！')
            return


e = threading.Event()                       # 创建事件对象
ex=threading.Thread(target=exit)            # 创建exit进程对象
ex.start()
ex.join()