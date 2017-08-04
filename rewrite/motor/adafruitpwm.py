from Adafruit_PWM_Servo_Driver import PWM

class AdafruitPWM:
    def __init__(self):
        # Initialise the PWM device
        pwm = PWM(0x40)
        pwm.setPWMFreq(60)

    def run(self, command):
        print "move adafruit pwm command", command

        if command == 'L':
            pwm.setPWM(1, 0, 300) # turn left
            pwm.setPWM(0, 0, 445) # drive forward
            time.sleep(0.5)
            pwm.setPWM(1, 0, 400) # turn neutral
            pwm.setPWM(0, 0, 335) # drive neutral

        elif command == 'R':
            pwm.setPWM(1, 0, 500) # turn right
            pwm.setPWM(0, 0, 445) # drive forward
            time.sleep(0.5)
            pwm.setPWM(1, 0, 400) # turn neutral
            pwm.setPWM(0, 0, 335) # drive neutral

        elif command == 'BL':
            pwm.setPWM(1, 0, 300) # turn left
            pwm.setPWM(0, 0, 270) # drive backward
            time.sleep(0.5)
            pwm.setPWM(1, 0, 400) # turn neutral
            pwm.setPWM(0, 0, 335) # drive neutral

        elif command == 'BR':
            pwm.setPWM(1, 0, 500) # turn right
            pwm.setPWM(0, 0, 270) # drive backward
            time.sleep(0.5)
            pwm.setPWM(1, 0, 400) # turn neurtral
            pwm.setPWM(0, 0, 335) # drive neutral


        elif command == 'F':
            pwm.setPWM(0, 0, 445) # drive forward
            time.sleep(0.3)
            pwm.setPWM(0, 0, 345) # drive slowly forward
            time.sleep(0.4)
            pwm.setPWM(0, 0, 335) # drive neutral
        elif command == 'B':
            pwm.setPWM(0, 0, 270) # drive backward
            time.sleep(0.3)
            pwm.setPWM(0, 0, 325) # drive slowly backward
            time.sleep(0.4)
            pwm.setPWM(0, 0, 335) # drive neutral

        elif command == 'S2INC': # neutral
            pwm.setPWM(2, 0, 300)

        elif command == 'S2DEC':
            pwm.setPWM(2, 0, 400)

        elif command == 'POS60':
            pwm.setPWM(2, 0, 490)

        elif command == 'NEG60':
            pwm.setPWM(2, 0, 100)
