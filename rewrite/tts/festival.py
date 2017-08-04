from tempfile import NamedTemporaryFile

class Festival:
    def say(message):
        tempfile = NamedTemporaryFile()
        tempfile.write(message)
        tempfile.flush()
        os.system('festival --tts < ' + tempfile.name)
        tempfile.close()
