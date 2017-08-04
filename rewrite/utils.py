# Object which is true after every <interval> seconds
# For Python2, use the __nonzero__ method
from time import time

class Every:
    def __init__(self, interval):
        self.interval = interval
        self.lasttime = time()

    def __bool__(self):
        current = time()
        if current-self.lasttime>=self.interval:
            self.lasttime = current
            return True
        return False

    def __nonzero__(self):
        return self.__bool__()

def watchdog():
    import os
    # watch dog timer
    os.system("sudo modprobe bcm2835_wdt")
    os.system("sudo /usr/sbin/service watchdog start")


def times(lst, number):
    return [x*number for x in lst]
