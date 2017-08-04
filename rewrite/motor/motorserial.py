import serial
class Serial:
    def __init__(self, serialDevice):
        #serialDevice = '/dev/tty.usbmodem12341'
        #serialDevice = '/dev/ttyUSB0'
        # initialize serial connection
        serialBaud = 9600
        print "baud:", serialBaud
        #ser = serial.Serial('/dev/tty.usbmodem12341', 19200, timeout=1)  # open serial
        ser = serial.Serial(serialDevice, serialBaud, timeout=1)  # open serial

    def run(self, command):

        print(ser.name)         # check which port was really used
        ser.nonblocking()

        # loop to collect input
        #s = "f"
        #print "string:", s
        print str(command.lower())
        ser.write(command.lower() + "\r\n")     # write a string
        #ser.write(s)
        ser.flush()

        #while ser.in_waiting > 0:
        #    print "read:", ser.read()

        #ser.close()
