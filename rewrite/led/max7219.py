import spidev

class Max7219:

    def __init__(self, ledrotate="0"):
        spi = spidev.SpiDev()
        spi.open(0,0)
        #VCC -> RPi Pin 2
        #GND -> RPi Pin 6
        #DIN -> RPi Pin 19
        #CLK -> RPi Pin 23
        #CS -> RPi Pin 24

        # decoding:BCD
        spi.writebytes([0x09])
        spi.writebytes([0x00])
        # Start with low brightness
        spi.writebytes([0x0a])
        spi.writebytes([0x03])
        # scanlimit; 8 LEDs
        spi.writebytes([0x0b])
        spi.writebytes([0x07])
        # Enter normal power-mode
        spi.writebytes([0x0c])
        spi.writebytes([0x01])
        # Activate display
        spi.writebytes([0x0f])
        spi.writebytes([0x00])
        self.columns = [0x1,0x2,0x3,0x4,0x5,0x6,0x7,0x8]
        self.LEDOn = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        self.LEDOff = [0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0]
        self.LEDEmoteSmile = [0x0,0x0,0x24,0x0,0x42,0x3C,0x0,0x0]
        self.LEDEmoteSad = [0x0,0x0,0x24,0x0,0x0,0x3C,0x42,0x0]
        self.LEDEmoteTongue = [0x0,0x0,0x24,0x0,0x42,0x3C,0xC,0x0]
        self.LEDEmoteSuprise = [0x0,0x0,0x24,0x0,0x18,0x24,0x24,0x18]
        if ledrotate == '180':
            self.LEDEmoteSmile = LEDEmoteSmile[::-1]
            self.LEDEmoteSad = LEDEmoteSad[::-1]
            self.LEDEmoteTongue = LEDEmoteTongue[::-1]
            self.LEDEmoteSuprise = LEDEmoteSuprise[::-1]

    def run(self, command):
        if command == 'LED_OFF':
            self.off()
        elif command == 'LED_FULL':
            self.on()
            self.full()
        elif command == 'LED_MED':
            self.on()
            self.med()
        elif command == 'LED_LOW':
            self.on()
            self.low()
        elif command == 'LED_E_SMILEY':
            self.on()
            self.e_smiley()
        elif command == 'LED_E_SAD':
            self.on()
            self.e_sad()
        elif command == 'LED_E_TONGUE':
            self.on()
            self.e_tongue()
        elif command == 'LED_E_SUPRISED':
            self.on()
            self.e_suprised()

    def on(self):
        for i,v in enumerate(self.columns):
            spi.xfer(v, self.LEDOn[i]])

    def off(self):
        for i,v in enumerate(self.columns):
            spi.xfer(v, self.LEDOff[i]])

    def e_smiley(self):
        for i,v in enumerate(self.columns):
            spi.xfer(v, self.LEDEmoteSmile[i]])

    def e_sad(self):
        for i,v in enumerate(self.columns):
            spi.xfer(v, self.LEDEmoteSad[i]])

    def e_tongue(self):
        for i,v in enumerate(self.columns):
            spi.xfer(v, self.LEDEmoteTongue[i]])

    def e_suprised(self):
        for i,v in enumerate(self.columns):
            spi.xfer(v, self.LEDEmoteSuprise[i]])

    def low(self):
        # brightness MIN
        spi.writebytes([0x0a])
        spi.writebytes([0x00])

    def med(self):
        #brightness MED
        spi.writebytes([0x0a])
        spi.writebytes([0x06])

    def full(self):
        # brightness MAX
        spi.writebytes([0x0a])
        spi.writebytes([0x0F])
