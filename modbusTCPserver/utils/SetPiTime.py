import shlex
import subprocess
import time

from _datetime import datetime


def linux_set_time(timestamp_give):
    timestamp_now = int(time.time())
    if timestamp_now < timestamp_give:
        datetime_give = datetime.fromtimestamp(timestamp_give)
        time_string = datetime_give.isoformat()
        # May be necessary
        subprocess.call(shlex.split("timedatectl set-ntp false"))
        subprocess.call(shlex.split("sudo date -s '%s'" % time_string))


if __name__ == '__main__':
    linux_set_time(1542102340)
