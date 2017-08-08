import gopigo
from motor import Motor
import time

class GoPiGo2(Motor):
    def __init__(self):
        pass

    def run(self, command):
        if command == 'L':
            gopigo.left_rot()
            time.sleep(0.15)
            gopigo.stop()
        elif command == 'R':
            gopigo.right_rot()
            time.sleep(0.15)
            gopigo.stop()
        elif command == 'F':
            gopigo.forward()
            time.sleep(0.35)
            gopigo.stop()
        elif command == 'B':
            gopigo.backward()
            time.sleep(0.35)
            gopigo.stop()
