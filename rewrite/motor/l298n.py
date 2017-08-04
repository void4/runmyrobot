import RPi.GPIO as GPIO

#Change sleeptime to adjust driving speed
#Change rotatetimes to adjust the rotation. Will be multiplicated with sleeptime.
l298n_sleeptime=0.2
l298n_rotatetimes=5

class L298N:

    def __init__(self):
        try:
            import configparser
        except ImportError:
            print "You need to install configparser (sudo python -m pip install configparser)\n Ctrl-C to quit"
            while True:
                pass # Halt program	to avoid error down the line.

        mode = GPIO.getmode()
        print " mode = "+str(mode)
        GPIO.cleanup()
        #Change the GPIO Pins to your connected motors in gpio.conf
        #visit http://bit.ly/1S5nQ4y for reference
        gpio_config = configparser.ConfigParser()
        gpio_config.read('gpio.conf')
        if str(robotID) in gpio_config.sections():
            config_id = str(robotID)
        else:
            config_id = 'default'

        StepPinForward = int(str(gpio_config[config_id]['StepPinForward']).split(',')[0]),int(str(gpio_config[config_id]['StepPinForward']).split(',')[1])
        StepPinBackward = int(str(gpio_config[config_id]['StepPinBackward']).split(',')[0]),int(str(gpio_config[config_id]['StepPinBackward']).split(',')[1])
        StepPinLeft = int(str(gpio_config[config_id]['StepPinLeft']).split(',')[0]),int(str(gpio_config[config_id]['StepPinLeft']).split(',')[1])
        StepPinRight = int(str(gpio_config[config_id]['StepPinRight']).split(',')[0]),int(str(gpio_config[config_id]['StepPinRight']).split(',')[1])

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(StepPinForward, GPIO.OUT)
        GPIO.setup(StepPinBackward, GPIO.OUT)
        GPIO.setup(StepPinLeft, GPIO.OUT)
        GPIO.setup(StepPinRight, GPIO.OUT)

    def run(self, command):
        if command == 'F':
            GPIO.output(StepPinForward, GPIO.HIGH)
            time.sleep(l298n_sleeptime * l298n_rotatetimes)
            GPIO.output(StepPinForward, GPIO.LOW)
        elif command == 'B':
            GPIO.output(StepPinBackward, GPIO.HIGH)
            time.sleep(l298n_sleeptime * l298n_rotatetimes)
            GPIO.output(StepPinBackward, GPIO.LOW)
        elif command == 'L':
            GPIO.output(StepPinLeft, GPIO.HIGH)
            time.sleep(l298n_sleeptime)
            GPIO.output(StepPinLeft, GPIO.LOW)
        elif command == 'R':
            GPIO.output(StepPinRight, GPIO.HIGH)
            time.sleep(l298n_sleeptime)
            GPIO.output(StepPinRight, GPIO.LOW)
