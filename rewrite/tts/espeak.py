from tempfile import NamedTemporaryFile

class Espeak:
    def say(message):
        tempfile = NamedTemporaryFile()
        tempfile.write(message)
        tempfile.flush()
        for hardwareNumber in (2, 0, 1):
            if commandArgs.male:
                os.system('cat ' + tempFilePath + ' | espeak --stdout | aplay -D plughw:%d,0' % hardwareNumber)
            else:
                os.system('cat ' + tempFilePath + ' | espeak -ven-us+f%d -s170 --stdout | aplay -D plughw:%d,0' % (commandArgs.voice_number, hardwareNumber))

        tempfile.close()
