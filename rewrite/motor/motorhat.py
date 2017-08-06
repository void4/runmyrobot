import datetime
import atexit
import getpass
import os

import RPi.GPIO as GPIO

from ..utils import Every
from motor import Motor

chargeValue = 0.0
secondsToCharge = 60 * 60 * 3
secondsToDischarge = 60 * 60 * 10


chargeIONumber = 17
turningSpeedActuallyUsed = 250
# every60 = Every(60) (not guaranteed, unless command is issued)

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

# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)
servoMin = [150, 150, 130]  # Min pulse length out of 4096
servoMax = [600, 600, 270]  # Max pulse length out of 4096
armServo = [300, 300, 300]

#def setMotorsToIdle():
#    s = 65
#    for i in range(1, 2):
#        mh.getMotor(i).setSpeed(s)
#        mh.getMotor(i).run(Adafruit_MotorHAT.FORWARD)

# Unused?
def setServoPulse(channel, pulse):
    pulseLength = 1000000                   # 1,000,000 us per second
    pulseLength /= 60                       # 60 Hz
    print "%d us per period" % pulseLength
    pulseLength /= 4096                     # 12 bits of resolution
    print "%d us per bit" % pulseLength
    pulse *= 1000
    pulse /= pulseLength
    pwm.setPWM(channel, 0, pulse)

def incrementArmServo(channel, amount):

    armServo[channel] += amount

    print "arm servo positions:", armServo

    if armServo[channel] > servoMax[channel]:
        armServo[channel] = servoMax[channel]
    if armServo[channel] < servoMin[channel]:
        armServo[channel] = servoMin[channel]
    pwm.setPWM(channel, 0, armServo[channel])

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

# true if it's on the charger and it needs to be charging
def isCharging():
    print("is charging current value", chargeValue)
    if chargeValue < 99:
        print("Charge value is low")
        return GPIO.input(chargeIONumber) == 1
    else:
        print("Charge value is high")
        return False

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

class MotorHat(Motor):
    def __init__(self, drivingSpeed, daySpeed, nightSpeed, forward, backward, left, right, straightDelay, turnDelay):

        self.drivingSpeed = drivingSpeed
        self.daySpeed = daySpeed
        self.nightSpeed = nightSpeed

        self.forward = forward
        self.backward = backward
        self.left = left
        self.right = right
        self.straightDelay = straightDelay
        self.turnDelay = turnDelay

        # todo: specificity is not correct, this is specific to a bot with a claw, not all motor_hat based bots
        from Adafruit_PWM_Servo_Driver import PWM
        # Initialise the PWM device
        pwm = PWM(0x42)
        pwm.setPWMFreq(60)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(chargeIONumber, GPIO.IN)

        self.sendChargeState = sendChargeState

    def run(self, command):
        now = datetime.datetime.now()
        now_time = now.time()
        # if it's late, make the robot slower
        if now_time >= datetime.time(21,30) or now_time <= datetime.time(9,30):
            #print "within the late time interval"
            drivingSpeedActuallyUsed = nightTimeDrivingSpeedActuallyUsed
        else:
            drivingSpeedActuallyUsed = dayTimeDrivingSpeedActuallyUsed

        if motorsEnabled:
            motorA.setSpeed(drivingSpeed)
            motorB.setSpeed(drivingSpeed)
            if command == 'F':
                drivingSpeed = drivingSpeedActuallyUsed
                for motorIndex in range(4):
                    runMotor(motorIndex, self.forward[motorIndex])
                time.sleep(self.straightDelay)
            elif command == 'B':
                drivingSpeed = drivingSpeedActuallyUsed
                for motorIndex in range(4):
                    runMotor(motorIndex, self.backward[motorIndex])
                time.sleep(self.straightDelay)
            elif command == 'L':
                drivingSpeed = turningSpeedActuallyUsed
                for motorIndex in range(4):
                    runMotor(motorIndex, self.left[motorIndex])
                time.sleep(self.turnDelay)
            elif command == 'R':
                drivingSpeed = turningSpeedActuallyUsed
                for motorIndex in range(4):
                    runMotor(motorIndex, self.right[motorIndex])
                time.sleep(self.turnDelay)
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

    def updateChargeApproximation(self):

        username = getpass.getuser()
        path = "/home/pi/charge_state_%s.txt" % username

        # read charge value
        # assume it is zero if no file exists
        if os.path.isfile(path):
            file = open(path, 'r')
            chargeValue = float(file.read())
            file.close()
        else:
            print("Setting charge value to zero")
            chargeValue = 0

        chargePerSecond = 1.0 / secondsToCharge
        dischargePerSecond = 1.0 / secondsToDischarge

        if GPIO.input(chargeIONumber) == 1:
            chargeValue += 100.0 * chargePerSecond * chargeCheckInterval
        else:
            chargeValue -= 100.0 * dischargePerSecond * chargeCheckInterval

        if chargeValue > 100.0:
            chargeValue = 100.0
        if chargeValue < 0:
            chargeValue = 0.0

        # write new charge value
        file = open(path, 'w')
        file.write(str(chargeValue))
        file.close()

        print "charge value updated to", chargeValue
