import shlex
import subprocess
import time

from _datetime import datetime


def linux_set_time(timestamp_give):
    """给定时间戳,设置linux系统时间

    Arguments:
        timestamp_give {int} -- uint32时间戳
    """

    timestamp_now = int(time.time())
    if timestamp_now < timestamp_give:  # 如果时间更靠后
        datetime_give = datetime.fromtimestamp(timestamp_give)
        time_string = datetime_give.isoformat()
        subprocess.call(shlex.split("timedatectl set-ntp false"))  # May be necessary 禁止自动更新时间
        subprocess.call(shlex.split("sudo date -s '%s'" % time_string))


if __name__ == '__main__':
    linux_set_time(1542102340)
