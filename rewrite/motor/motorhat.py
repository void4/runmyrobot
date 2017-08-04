import RPi.GPIO as GPIO
import atexit

try:
    from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
    motorsEnabled = True
except ImportError:
    print "You need to install Adafruit_MotorHAT"
    print "Please install Adafruit_MotorHAT for python and restart this script."
    print "To install: cd /usr/local/src && sudo git clone https://github.com/adafruit/Adafruit-Motor-HAT-Python-Library.git"
    print "cd /usr/local/src/Adafruit-Motor-HAT-Python-Library && sudo python setup.py install"
    print "Running in test mode."
    print "Ctrl-C to quit"
    motorsEnabled = False

def runMotor(motorIndex, direction):
    motor = mh.getMotor(motorIndex+1)
    if direction == 1:
        motor.setSpeed(drivingSpeed)
        motor.run(Adafruit_MotorHAT.FORWARD)
    if direction == -1:
        motor.setSpeed(drivingSpeed)
        motor.run(Adafruit_MotorHAT.BACKWARD)
    if direction == 0.5:
        motor.setSpeed(128)
        motor.run(Adafruit_MotorHAT.FORWARD)
    if direction == -0.5:
        motor.setSpeed(128)
        motor.run(Adafruit_MotorHAT.BACKWARD)

if motorsEnabled:
    # create a default object, no changes to I2C address or frequency
    mh = Adafruit_MotorHAT(addr=0x60)
    #mhArm = Adafruit_MotorHAT(addr=0x61)


def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
    #mhArm.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    #mhArm.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    #mhArm.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    #mhArm.getMotor(4).run(Adafruit_MotorHAT.RELEASE)


if motorsEnabled:
    atexit.register(turnOffMotors)
    motorA = mh.getMotor(1)
    motorB = mh.getMotor(2)

def sendChargeState():
    charging = isCharging()
    chargeState = {'robot_id': robotID, 'charging': charging}
    socketIO.emit('charge_state', chargeState)
    print "charge state:", chargeState

def sendChargeStateCallback(x):
    sendChargeState()

if commandArgs.type == 'motor_hat':
    GPIO.add_event_detect(chargeIONumber, GPIO.BOTH)
    GPIO.add_event_callback(chargeIONumber, sendChargeStateCallback)

class MotorHat:
    def __init__(self):

        # todo: specificity is not correct, this is specific to a bot with a claw, not all motor_hat based bots
        from Adafruit_PWM_Servo_Driver import PWM
        # Initialise the PWM device
        pwm = PWM(0x42)
        pwm.setPWMFreq(60)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(chargeIONumber, GPIO.IN)

    def run(self, command):
        if motorsEnabled:
            motorA.setSpeed(drivingSpeed)
            motorB.setSpeed(drivingSpeed)
            if command == 'F':
                drivingSpeed = drivingSpeedActuallyUsed
                for motorIndex in range(4):
                    runMotor(motorIndex, forward[motorIndex])
                time.sleep(straightDelay)
            elif command == 'B':
                drivingSpeed = drivingSpeedActuallyUsed
                for motorIndex in range(4):
                    runMotor(motorIndex, backward[motorIndex])
                time.sleep(straightDelay)
            elif command == 'L':
                drivingSpeed = turningSpeedActuallyUsed
                for motorIndex in range(4):
                    runMotor(motorIndex, left[motorIndex])
                time.sleep(turnDelay)
            elif command == 'R':
                drivingSpeed = turningSpeedActuallyUsed
                for motorIndex in range(4):
                    runMotor(motorIndex, right[motorIndex])
                time.sleep(turnDelay)
            elif command == 'U':
                #mhArm.getMotor(1).setSpeed(127)
                #mhArm.getMotor(1).run(Adafruit_MotorHAT.BACKWARD)
                incrementArmServo(1, 10)
                time.sleep(0.05)
            elif command == 'D':
                #mhArm.getMotor(1).setSpeed(127)
                #mhArm.getMotor(1).run(Adafruit_MotorHAT.FORWARD)
                incrementArmServo(1, -10)
                time.sleep(0.05)
            elif command == 'O':
                #mhArm.getMotor(2).setSpeed(127)
                #mhArm.getMotor(2).run(Adafruit_MotorHAT.BACKWARD)
                incrementArmServo(2, -10)
                time.sleep(0.05)
            elif command == 'C':
                #mhArm.getMotor(2).setSpeed(127)
                #mhArm.getMotor(2).run(Adafruit_MotorHAT.FORWARD)
                incrementArmServo(2, 10)
                time.sleep(0.05)

        turnOffMotors()
