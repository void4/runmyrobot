import os

class Audio:
    def __init__(self, tts_volume):
        self.tts_volume = tts_volume
        # set volume level
        # tested for 3.5mm audio jack
        if self.tts_volume > 50:
            os.system("amixer set PCM -- -100")

        # tested for USB audio device
        os.system("amixer -c 2 cset numid=3 %d%%" % self.tts_volume)

    def changeVolumeHighThenNormal(self):

        os.system("amixer -c 2 cset numid=3 %d%%" % 100)
        time.sleep(25)
        os.system("amixer -c 2 cset numid=3 %d%%" % self.tts_volume)
