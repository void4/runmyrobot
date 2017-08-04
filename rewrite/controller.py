import platform
import json
import re
import sys
import argparse
import thread
import subprocess

parser = argparse.ArgumentParser(description='start robot control program')
parser.add_argument('robot_id', help='Robot ID')
parser.add_argument('--env', help="Environment for example dev or prod, prod is default", default='prod')
parser.add_argument('--type', help="serial or motor_hat or gopigo2 or gopigo3 or l298n or motozero or pololu", default='motor_hat')
parser.add_argument('--serial-device', help="serial device", default='/dev/ttyACM0')
parser.add_argument('--male', dest='male', action='store_true')
parser.add_argument('--female', dest='male', action='store_false')
parser.add_argument('--voice-number', type=int, default=1)
parser.add_argument('--led', help="Type of LED for example max7219", default=None)
parser.add_argument('--ledrotate', help="Rotates the LED matrix. Example: 180", default=None)
parser.add_argument('--tts-volume', type=int, default=80)
parser.add_argument('--secret-key', default=None)
parser.add_argument('--turn-delay', type=float, default=0.4)
parser.add_argument('--straight-delay', type=float, default=0.5)
parser.add_argument('--driving-speed', type=int, default=90)
parser.add_argument('--day-speed', type=int, default=255)
parser.add_argument('--night-speed', type=int, default=255)
parser.add_argument('--forward', default='[-1,1,-1,1]')
parser.add_argument('--left', default='[1,1,1,1]')
parser.add_argument('--festival-tts', dest='festival_tts', action='store_true')
parser.set_defaults(festival_tts=False)
parser.add_argument('--auto-wifi', dest='auto_wifi', action='store_true')
parser.set_defaults(auto_wifi=False)
parser.add_argument('--no-anon-tts', dest='anon_tts', action='store_false')
parser.set_defaults(anon_tts=True)
parser.add_argument('--filter-url-tts', dest='filter_url_tts', action='store_true')
parser.set_defaults(filter_url_tts=False)
commandArgs = parser.parse_args()
print commandArgs

from socketIO_client import SocketIO, LoggingNamespace

from net import net
from utils import Every, watchdog, times
from audio.audio import Audio

watchdog()
audio = Audio(commandArgs.tts_volume)

server = "runmyrobot.com"
#server = "52.52.213.92"

if commandArgs.env == 'dev':
    print 'DEV MODE ***************'
    print "using dev port 8122"
    port = 8122
elif commandArgs.env == 'prod':
    print 'PROD MODE *************'
    print "using prod port 8022"
    port = 8022
else:
    print "invalid environment"
    sys.exit(0)

print 'using socket io to connect to', server
socketIO = SocketIO(server, port, LoggingNamespace)
print 'finished using socket io to connect to', server

# motor controller specific intializations

modules = []

if commandArgs.type == 'none':
    from motor.motor import Motor
    modules.append(Motor())
elif commandArgs.type == "dummy":
    from motor.motor import DummyMotor
    modules.append(DummyMotor())
elif commandArgs.type == 'motor_hat':
    from motor.motorhat import MotorHat
    forward = json.loads(commandArgs.forward)
    backward = times(forward, -1)
    left = json.loads(commandArgs.left)
    right = times(left, -1)
    straightDelay = commandArgs.straight_delay
    turnDelay = commandArgs.turn_delay
    modules.append(MotorHat(commandArgs.driving_speed, commandArgs.day_speed, commandArgs.night_speed, forward, backward, left, right, straightDelay, turnDelay))
elif commandArgs.type == 'gopigo2':
    from motor.gopigo2 import GoPiGo2
    modules.append(GoPiGo2())
elif commandArgs.type == 'gopigo3':
    from motor.gopigo3 import GoPiGo3
    modules.append(GoPiGo3())
elif commandArgs.type == 'l298n':
    from motor.l298n import L298N
    modules.append(L298N())
elif commandArgs.type == 'motozero':
    from motor.motozero import MotoZero
    modules.append(MotoZero())
elif commandArgs.type == 'pololu':
    from motor.pololu import Pololu
    modules.append(Pololu())
elif commandArgs.type == 'screencap':
    pass
elif commandArgs.type == 'adafruit_pwm':
    from motor.adafruitpwm import AdafruitPWM
    modules.append(AdafruitPWM())
elif commandArgs.type == 'serial':
    from motor.motorserial import Serial
    modules.append(Serial(commandArgs.serial_device))
else:
    print "invalid --type in command line"
    exit(0)

uistring = [{"button_panels": []}]

responses = []
for module in modules:
    response = module.ui()

    if not response:
        continue
    elif isinstance(response, str):
        response = json.loads(response)
    elif not isinstance(response, dict):
        print("Module", module, "returned invalid response")
        continue

    responses.append(response)

from ui import setCustomUI
if responses:
    uistring[0]["button_panels"] += responses
    print(uistring)
    setCustomUI(commandArgs.robot_id, uistring)

#LED controlling
if commandArgs.led == 'max7219':
    from led.max7219 import Max7219
    led = Max7219()
    led.off()
    modules.append(led)
elif commandArgs.led is not None:
    print("%s not yet supported!" % commandArgs.led)

handlingCommand = False

def handle_exclusive_control(args):
        if 'status' in args and 'robot_id' in args and args['robot_id'] == commandArgs.robot_id:

            status = args['status']

        if status == 'start':
                print "start exclusive control"
        if status == 'end':
                print "end exclusive control"

if commandArgs.festival_tts:
    from tts.festival import Festival
    tts = Festival()
else:
    from tts.espeak import Espeak
    tts = Espeak()

def handle_chat_message(args):

    print "chat message received:", args
    rawMessage = args['message']
    withoutName = rawMessage.split(']')[1:]
    message = "".join(withoutName)
    urlRegExp = "(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
    if message[1] == ".":
        exit()
    elif commandArgs.anon_tts != True and args['anonymous'] == True:
        exit()
    elif commandArgs.filter_url_tts == True and re.search(urlRegExp, message):
        exit()
    else:
        tts.say(message)

def handle_command(args):
        global handlingCommand

        if 'robot_id' in args and args['robot_id'] == commandArgs.robot_id:
            print "received message:", args
        # Note: If you are adding features to your bot,
        # you can get direct access to incomming commands right here.

        if handlingCommand:
            return

        handlingCommand = True

        if 'command' in args and 'robot_id' in args and args['robot_id'] == commandArgs.robot_id:

            print('got command', args)

            command = args['command']

            if command == 'LOUD':
                thread.start_new_thread(audio.changeVolumeHighThenNormal, ())

            for module in modules:
                module.run(command)
            #setMotorsToIdle()

        handlingCommand = False

def handleStartReverseSshProcess(args):
    print "starting reverse ssh"
    socketIO.emit("reverse_ssh_info", "starting")
    returnCode = subprocess.call(["/usr/bin/ssh", "-X", "-i", "/home/pi/reverse_ssh_key1.pem", "-N", "-R", "2222:localhost:22", "ubuntu@52.52.204.174"])
    socketIO.emit("reverse_ssh_info", "return code: " + str(returnCode))
    print "reverse ssh process has exited with code", str(returnCode)

def handleEndReverseSshProcess(args):
    print "handling end reverse ssh process"
    resultCode = subprocess.call(["killall", "ssh"])
    print "result code of killall ssh:", resultCode

def on_handle_command(*args):
   thread.start_new_thread(handle_command, args)

def on_handle_exclusive_control(*args):
   thread.start_new_thread(handle_exclusive_control, args)

def on_handle_chat_message(*args):
   thread.start_new_thread(handle_chat_message, args)

socketIO.on('command_to_robot', on_handle_command)
socketIO.on('exclusive_control', on_handle_exclusive_control)
socketIO.on('chat_message_with_name', on_handle_chat_message)

def startReverseSshProcess(*args):
   thread.start_new_thread(handleStartReverseSshProcess, args)

def endReverseSshProcess(*args):
   thread.start_new_thread(handleEndReverseSshProcess, args)

socketIO.on('reverse_ssh_8872381747239', startReverseSshProcess)
socketIO.on('end_reverse_ssh_8872381747239', endReverseSshProcess)

def identifyRobotId():
    socketIO.emit('identify_robot_id', commandArgs.robot_id);

lastInternetStatus = False
chargeCheckInterval = 1
everyChargeCheck = Every(chargeCheckInterval)
every10 = Every(10)
every60 = Every(60)
every1000 = Every(1000)

while True:

    #if motor and everyChargeCheck:
    #    motor.updateChargeApproximation()

    if every10:
        if commandArgs.auto_wifi:
            if commandArgs.secret_key is not None:
                net.configWifiLogin(commandArgs.secret_key)

    if every60:
        # tell the server what robot id is using this connection
        identifyRobotId()

        if platform.system() == 'Linux':
            socketIO.emit('ip_information',
                      {'ip': subprocess.check_output(["hostname", "-I"]), 'robot_id': commandArgs.robot_id})

        #if commandArgs.type == 'motor_hat':
        #    motor.sendChargeState()

    if every1000:
        internetStatus = net.isInternetConnected()
        if internetStatus != lastInternetStatus:
            if internetStatus:
                tts.say("ok")
            else:
                tts.say("missing internet connection")
        lastInternetStatus = internetStatus

    socketIO.wait(seconds=0.5)
