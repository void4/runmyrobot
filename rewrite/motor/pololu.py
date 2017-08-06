from motor import Motor

try:
    from pololu_drv8835_rpi import motors, MAX_SPEED
except ImportError:
	print "You need to install drv8835-motor-driver-rpi"
    print "Please install drv8835-motor-driver-rpi for python and restart this script."
    print "To install: cd /usr/local/src && sudo git clone https://github.com/pololu/drv8835-motor-driver-rpi"
    print "cd /usr/local/src/drv8835-motor-driver-rpi && sudo python setup.py install"
    print "Running in test mode."
    print "Ctrl-C to quit"

class Pololu(Motor):
    def __init__(self):
        pass

    def run(self, command):
        drivingSpeed = self.drivingSpeed
        if command == 'F':
    	      motors.setSpeeds(drivingSpeed, drivingSpeed)
    	      time.sleep(0.3)
    	      motors.setSpeeds(0, 0)
        elif command == 'B':
    	      motors.setSpeeds(-drivingSpeed, -drivingSpeed)
    	      time.sleep(0.3)
    	      motors.setSpeeds(0, 0)
        elif command == 'L':
    	      motors.setSpeeds(-drivingSpeed, drivingSpeed)
    	      time.sleep(0.3)
    	      motors.setSpeeds(0, 0)
        elif command == 'R':
    	      motors.setSpeeds(drivingSpeed, -drivingSpeed)
    	      time.sleep(0.3)
    	      motors.setSpeeds(0, 0)
