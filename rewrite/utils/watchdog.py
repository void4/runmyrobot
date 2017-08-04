import os
# watch dog timer
os.system("sudo modprobe bcm2835_wdt")
os.system("sudo /usr/sbin/service watchdog start")
